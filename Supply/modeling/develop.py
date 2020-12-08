import logging
import numpy
# from tqdm import tqdm
import random
from multiprocessing import Pool, cpu_count
import copy
import math
import time

from modeling.candidates import create_candidate_set
from modeling.filters import apply_filters, acreage_available
from modeling.dataframe_updates import update_mgra, increment_building_ages

from utils.access_labels import all_product_type_labels
from utils.interface import parameters
from utils.pandas_shortcuts import running_average


def buildable_units(candidate, product_type_labels, max_units):
    # determine max units to build
    vacancy_cap = candidate.vacancy_cap.item()

    # FIXME: possibly use profitability filter value for this mgra
    # to determine the number of profitable units to build.

    # only build up to 95% of the vacant space
    acreage = acreage_available(candidate, product_type_labels)
    acreage_per_unit = product_type_labels.land_use_per_unit_parameter()
    available_units_by_land = acreage.values.item() * \
        0.95 // acreage_per_unit

    logging.debug('max: {}, vacancy: {}, by land: {}'.format(
        max_units, vacancy_cap, available_units_by_land))
    return int(min(max_units,
                   vacancy_cap, available_units_by_land))


def normalize(collection):
    # works with pandas Series and numpy arrays
    return collection / collection.sum()


def combine_weights(profitability, vacancy):
    '''
        Uses profitability and total units allowed by vacancy to make
        normalized weights,
        deference for vacancy, as modified by parameter scale multiplier.
    '''
    mnl_choice = parameters['use_choice_model']
    scale = parameters['scale']

    if mnl_choice:
        exponent_profitability = numpy.exp(scale*profitability)
        weights = vacancy * exponent_profitability
    else:
        # Simple weighting
        weights = vacancy + (scale * profitability)

    return normalize(weights)


def choose_candidate(candidates, mgras, product_type_labels, max_units):
    # Filter
    filtered = apply_filters(
        candidates, product_type_labels)
    if len(filtered) < 1:
        print('out of suitable mgras for product type {}'.format(
            product_type_labels.product_type))
        print('evaluate filtering methods...\nexiting')
        return None

    # !
    # save_to_file(filtered, 'data/output', 'filtered_candidates.csv')
    # return

    # Sample
    weights = combine_weights(filtered.profit_margin, filtered.vacancy_cap)
    selected_candidate = filtered.sample(n=1, weights=weights)

    buildable_count = buildable_units(
        selected_candidate, product_type_labels, max_units)

    # develop buildable_count units by updating the MGRA in the original
    # dataframe
    removed_units_reference = update_mgra(mgras, selected_candidate,
                                          buildable_count, product_type_labels,
                                          scheduled_development=False)

    return buildable_count, removed_units_reference


def demand_unsatisfied(demand):
    return demand[0] < demand[1]


def demands_unsatisfied(labels_demands):
    for _, demand in labels_demands:
        if demand_unsatisfied(demand):
            return True
    return False


def sum_demand(labels_demands):
    total = 0
    for _, demand in labels_demands:
        total += demand[1]
    return total


def update_labels_demand(labels, demand, difference):
    return (
        labels, (demand[0] + difference, demand[1])
    )


def find_product_type_in_labels_demand(labels_demand_list, product_type):
    for index, (labels, demand) in enumerate(labels_demand_list):
        if labels.product_type == product_type:
            return index
    print('could not find product type: {}'.format(product_type))
    return None


def subtract_from_fulfilled_demand(labels_demands, removed_units_reference):
    index_to_subtract_from = \
        find_product_type_in_labels_demand(
            labels_demands,
            removed_units_reference[0].product_type
        )
    labels_demands[index_to_subtract_from] = \
        update_labels_demand(
        labels_demands[index_to_subtract_from][0],
        labels_demands[index_to_subtract_from][1],
        removed_units_reference[1]
    )
    return labels_demands


def prep_demand():
    labels_demands = []
    for product_type_labels in all_product_type_labels():
        units_required = product_type_labels.units_per_year_parameter()
        if units_required < 0:
            units_required = 0
        # nested tuple with (appropriate labels for the product type,
        # (amount of demand fulfilled,
        # number of units needed total to fulfill demand))
        labels_demands.append((
            product_type_labels,
            (0, units_required)
        ))
    return labels_demands


def simulation_process(mgras, candidates, labels_demands):
    # progress_bar = tqdm(total=sum_demand(labels_demands))
    # progress_bar.set_description(
    # 'allocating units by alternating through each product type')
    # select one build candidate at a time for each product type
    while demands_unsatisfied(labels_demands):
        random.shuffle(labels_demands)
        for index, (labels, demand) in enumerate(labels_demands):
            if demand_unsatisfied(demand):
                built_demand, removed_units_reference = \
                    choose_candidate(
                        candidates,
                        mgras, labels, demand[1] - demand[0]
                    )
                if removed_units_reference is not None:
                    # redevelopment removed units, subtract from
                    # the appropriate demand progress
                    labels_demands = subtract_from_fulfilled_demand(
                        labels_demands, removed_units_reference)
                    # progress_bar.update(removed_units_reference[1])

                labels_demands[index] = update_labels_demand(
                    labels, demand, built_demand)
                # progress_bar.update(built_demand)
    return mgras
    # progress_bar.close()


def guesstimate_simulation_runtime(normal_runtime, runs, expected_threads):
    '''
    expects positive numbers for each argument.
    '''
    estimated_runtime = normal_runtime
    multiplier = math.ceil(runs / expected_threads)
    return estimated_runtime * multiplier


def develop(mgras, runs=1):
    """
    Arguments
        mgras:
            A pandas dataframe of mgra's that will be allocated new units
            based on demand inputs found in parameters.yaml
    Returns:
        a pandas dataframe with selected MGRA's updated
    """
    runs = parameters['runs']
    current_results = None
    shared_candidates = create_candidate_set(mgras)

    arg_lists = []
    for i in range(runs):
        arg_lists.append(
            (
                mgras.copy(), shared_candidates.copy(),
                copy.deepcopy(prep_demand())
            )
        )
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
    # add to housing age
    increment_building_ages(current_results)

    return current_results
