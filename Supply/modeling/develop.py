import logging
import numpy
from tqdm import tqdm
import random

from modeling.filters import apply_filters, acreage_available
from modeling.dataframe_updates import update_mgra, increment_building_ages

from utils.access_labels import all_product_type_labels
from utils.interface import parameters

from modeling.candidates import create_candidate_set


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

    return mgras, buildable_count, removed_units_reference


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


def develop(mgras):
    """
    Arguments
        mgras:
            A pandas dataframe of mgra's that will be updated with new values
            based on demand inputs found in parameters.yaml
    Returns:
        a pandas dataframe with selected MGRA's updated
    """
    # get candidate set
    candidates = create_candidate_set(mgras)

    # prep demand
    labels_demands = []
    for product_type_labels in all_product_type_labels():
        units_required = product_type_labels.units_per_year_parameter()
        if units_required < 0:
            units_required = 0
        labels_demands.append((
            product_type_labels,
            (0, units_required)
        ))

    progress_bar = tqdm(total=sum_demand(labels_demands))
    progress_bar.set_description(
        'allocating units by alternating through each product type')
    # select one build candidate at a time for each product type
    while demands_unsatisfied(labels_demands):
        random.shuffle(labels_demands)
        for index, (labels, demand) in enumerate(labels_demands):
            if demand_unsatisfied(demand):
                mgras, built_demand, removed_units_reference = \
                    choose_candidate(
                        candidates,
                        mgras, labels, demand[1] - demand[0]
                    )
                if removed_units_reference is not None:
                    # redevelopment removed units, subtract that value from
                    # the appropriate demand
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
                    progress_bar.update(removed_units_reference[1])
                labels_demands[index] = update_labels_demand(
                    labels, demand, built_demand)
                progress_bar.update(built_demand)

    progress_bar.close()
    # add to housing age
    increment_building_ages(mgras)

    return mgras
