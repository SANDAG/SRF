import logging
import numpy
from tqdm import tqdm
import random

from modeling.filters import apply_filters, generic_filter, acreage_available
from modeling.dataframe_updates import update_mgra
from utils.access_labels import all_product_type_labels, \
    mgra_labels
from modeling.candidates import create_candidate_set


def buildable_units(mgra, product_type_labels, max_units, vacancy_caps):
    # determine max units to build
    vacancy_cap = vacancy_caps.loc[mgra.index].values.item()

    # FIXME: possibly use profitability filter value for this mgra
    # to determine the number of profitable units to build.

    # only build up to 95% of the vacant space
    acreage = acreage_available(mgra, product_type_labels)
    acreage_per_unit = product_type_labels.land_use_per_unit_parameter()
    available_units_by_land = acreage.values.item() * \
        0.95 // acreage_per_unit

    logging.debug('max: {}, vacancy: {}, by land {}'.format(
        max_units, vacancy_cap, available_units_by_land))
    return int(min(max_units,
                   vacancy_cap, available_units_by_land))


def normalize(collection):
    # works with pandas Series and numpy arrays
    return collection / collection.sum()


def combine_weights(profitability, vacancy, preference=0.5, mnl_choice=True):
    '''
        Uses profitability and total units allowed by vacancy to make
        normalized weights,
        deference for vacancy, as modified by preference multiplier.
    '''
    if mnl_choice:
        profitability = numpy.exp(profitability)
        weights = vacancy * preference * profitability
    else:
        weights = vacancy * preference + profitability

    return normalize(weights)


def choose_candidate(candidates, mgras, product_type_labels, max_units):
    # Filter
    filtered, vacancy_caps, profit_margins = apply_filters(
        candidates, product_type_labels)
    if len(filtered) < 1:
        print('out of usable mgras for product type {}'.format(
            product_type_labels.product_type))
        print('evaluate filtering methods\nexiting')
        return None

    # !
    # save_to_file(filtered, 'data/output', 'filtered_candidates.csv')
    # return

    # Sample
    weights = combine_weights(profit_margins, vacancy_caps)
    selected_candidate = filtered.sample(n=1, weights=weights)

    buildable_count = buildable_units(
        selected_candidate, product_type_labels, max_units, vacancy_caps)

    # develop buildable_count units by updating the MGRA in the original
    # dataframe
    # TODO replace selected id with the candidate row
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
    # create candidate set
    candidates = mgras.copy()
    # remove candidates with no vacant land ( 23002 to 8802)
    candidates = generic_filter(candidates, [mgra_labels.VACANT_ACRES])
    candidates = create_candidate_set(candidates)
    # prep demand
    labels_demands = []
    for product_type_labels in all_product_type_labels():
        units_required = product_type_labels.units_per_year_parameter()
        if units_required > 0:
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
    return mgras
