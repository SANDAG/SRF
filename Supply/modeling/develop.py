import logging
from multiprocessing import Pool, cpu_count
import copy
import math
import time
from tqdm import tqdm

from modeling.candidates import Candidates, candidate_development_type, \
    get_square_footage_per_unit, get_acreage_per_unit
from modeling.filters import acreage_available
from modeling.dataframe_updates import update_mgra, increment_building_ages
from modeling.demand_manager import DemandManager

from utils.access_labels import land_origin_labels
from utils.parameter_access import parameters
from utils.pandas_shortcuts import running_average


def redevelopment_check(candidate, product_type_labels):
    '''
    ensure that there are enough of the source fields for redevelopment
    to take place.
    returns: the maximum number of new destination units allowed by this check
    '''
    # find the source type
    development_label = candidate_development_type(
        candidate, product_type_labels)
    dev_type = land_origin_labels.label_type(development_label)
    if dev_type.redev:
        logging.debug('redev check: dev label: {}'.format(development_label))
        source_labels = land_origin_labels.get_origin(development_label)
        if source_labels is None:
            return None
        # start with just the source units count, others ~should~ be irrelevant
        maximum_source_units = candidate[source_labels.total_units].item()
        logging.debug('source units count: {}'.format(maximum_source_units))
        # # find the max source units allowed to be removed by square footage,
        # total acreage,
        # # product type acreage and units

        # translate the maximum amount of source units allowed to be
        # removed to the maximum number of units of destination to be built
        # by converting to squarefeet.
        current_square_footage = candidate[source_labels.square_footage].item()
        destination_sqft_per_unit = get_square_footage_per_unit(
            candidate, product_type_labels)
        available_units = current_square_footage / destination_sqft_per_unit
        return min(available_units, maximum_source_units)
    else:
        return None


def buildable_units(candidate, product_type_labels, max_units):
    # determine max units to build
    vacancy_cap = candidate.vacancy_cap.item()

    # FIXME: possibly use profitability filter value for this mgra
    # to determine the number of profitable units to build.

    # only build up to 95% of the vacant space
    acreage = acreage_available(candidate, product_type_labels)
    acreage_per_unit = get_acreage_per_unit(candidate, product_type_labels)
    available_units_by_land = acreage.values.item() * \
        0.95 // acreage_per_unit

    logging.debug('expected acreage available: {}'.format(acreage))
    logging.debug('max: {}, vacancy: {}, by land: {}'.format(
        max_units, vacancy_cap, available_units_by_land))
    maximums = [max_units, vacancy_cap, available_units_by_land]
    # also limit by redevelopment source available
    max_redevelopment_available = redevelopment_check(
        candidate, product_type_labels)
    if max_redevelopment_available is not None:
        logging.debug('redevelopment limited to {} units'.format(
            max_redevelopment_available))
        maximums.append(max_redevelopment_available)
    # return the lowest of all limits
    return int(min(maximums))


def choose_candidate(candidates, mgras, product_type_labels, max_units):
    selected_candidate = candidates.select_candidate_for_product_type(
        product_type_labels.product_type)
    if selected_candidate is None:
        logging.error(
            'out of suitable mgra candidates for product type {}'.format(
                product_type_labels.product_type))
        logging.error('evaluate input data and/or filtering methods...')
        logging.error('setting remaining demand for {} to zero'.format(
            product_type_labels.product_type))
        return None, None
    logging.debug('selected candidate: {}'.format(selected_candidate))
    buildable_count = buildable_units(
        selected_candidate, product_type_labels, max_units)
    if buildable_count < 1:
        return 0, None
    # develop buildable_count units on the selected MGRA by updating it in the
    # original dataframe
    removed_units_reference = update_mgra(
        mgras, selected_candidate,
        buildable_count, product_type_labels,
        scheduled_development=False, candidates=candidates.candidates)

    return buildable_count, removed_units_reference


def simulation_process(mgras, candidates, demand_manager, show_progress=False):
    if show_progress:
        progress_bar = tqdm(total=demand_manager.sum_demand())
        progress_bar.set_description(
            'allocating units by alternating through each product type')
    # select one build candidate at a time for each product type
    while demand_manager.demands_unsatisfied():
        for labels, demand in demand_manager.random_order_items():
            if demand.demand_unsatisfied():
                built_demand, removed_units_reference = \
                    choose_candidate(
                        candidates,
                        mgras, labels, demand.remaining_demand()
                    )
                if removed_units_reference is not None:
                    # redevelopment removed units, subtract from
                    # the appropriate demand progress
                    demand_manager.subtract_from_fulfilled_demand(
                        removed_units_reference[0], removed_units_reference[1]
                    )
                    if show_progress:
                        progress_bar.update(removed_units_reference[1])

                demand_manager.update_labels_demand(labels, built_demand)
                if built_demand is None:
                    candidates.remove_redev_from(labels)

                if show_progress and built_demand is not None:
                    progress_bar.update(built_demand)
    if show_progress:
        progress_bar.close()
    return mgras


def guesstimate_simulation_runtime(normal_runtime, runs, expected_threads):
    '''
    expects positive numbers for each argument.
    '''
    estimated_runtime = normal_runtime
    multiplier = math.ceil(runs / expected_threads)
    return estimated_runtime * multiplier


def perform_multiple_runs(mgras, current_results, shared_candidates, runs):
    arg_lists = [(
        mgras.copy(), copy.deepcopy(shared_candidates),
        copy.deepcopy(DemandManager())
    ) for _ in range(runs)
    ]
    normal_runtime = 60  # seconds
    eta = guesstimate_simulation_runtime(normal_runtime, runs, cpu_count())
    print(
        'queueing {} simulation runs on {}(?) cpu\'s. ETA: {} seconds...'
        .format(
            runs, cpu_count(), eta))
    with Pool() as pool:
        result = pool.starmap_async(simulation_process, arg_lists)
        slept = 0
        while not result.ready():
            sleep_time = 10
            time.sleep(sleep_time)
            slept += sleep_time
            print('time elapsed: {} seconds.'.format(slept))
        results = result.get(eta*3)

        pool.close()
        pool.join()
    i = 0
    for result in results:
        if current_results is None:
            current_results = result.copy()
            i = 1
        else:
            current_results, _ = running_average(
                current_results.copy(), i, result)
            i += 1
    # make mgra and luz ids integers again
    current_results = current_results.astype({'MGRA': 'int32', 'LUZ': 'int32'})
    return current_results


def develop(mgras, runs=None):
    """
    Arguments
        mgras:
            A pandas dataframe of mgra's that will be allocated new units
            based on demand inputs found in parameters.yaml
    Returns:
        a pandas dataframe with selected MGRA's updated
    """
    if runs is None:
        runs = parameters['runs']
    current_results = None
    shared_candidates = Candidates(mgras)

    if runs == 1:
        current_results = simulation_process(
            mgras, shared_candidates, DemandManager(), show_progress=True)
    else:
        current_results = perform_multiple_runs(
            mgras, current_results, shared_candidates, runs)
    # add to housing age
    increment_building_ages(current_results)

    return current_results
