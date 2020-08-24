import logging
import numpy
from tqdm import tqdm
import random
import copy

from modeling.filters import apply_filters, generic_filter
from modeling.dataframe_updates import update_mgra
from utils.access_labels import all_product_type_labels, \
    mgra_labels
from modeling.candidates import make_redev_candidates, trim_columns


def buildable_units(mgra, product_type_labels, max_units, vacancy_caps):
    acreage_per_unit = product_type_labels.land_use_per_unit_parameter()
    # determine max units to build
    vacancy_cap = vacancy_caps.loc[mgra.index].values.item()

    # TODO: also use profitability filter value for this mgra
    # to determine the number of profitable units to build.

    # only build up to 95% of the vacant space
    available_units_by_land = mgra[
        product_type_labels.vacant_acres].values.item() * \
        0.95 // acreage_per_unit

    logging.debug('max: {}, vacancy: {}, by land {}'.format(
        max_units, vacancy_cap, available_units_by_land))
    return int(min(max_units,
                   vacancy_cap, available_units_by_land))


def normalize(collection):
    # works with pandas Series and numpy arrays
    return collection / collection.sum()


def combine_weights(profitability, vacancy, preference=1):
    '''
        Prioritizes profitability to make selections, with some
        deference for vacancy, as modified by preference multiplier.
    '''
    weights = vacancy * preference * numpy.exp(profitability)
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

    # Sample
    weights = combine_weights(profit_margins, vacancy_caps)
    selected_row = filtered.sample(n=1, weights=weights)
    selected_ID = selected_row[mgra_labels.MGRA].iloc[0]

    buildable_count = buildable_units(
        selected_row, product_type_labels, max_units, vacancy_caps)
    logging.debug('building {} {} units on MGRA #{}'.format(
        buildable_count, product_type_labels.product_type, selected_ID))

    # develop buildable_count units by updating the MGRA in the dataframe
    update_mgra(mgras, selected_ID,
                buildable_count, product_type_labels)

    return mgras, buildable_count


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
    # candidate_set = CandidateSet(mgras)
    candidates = copy.deepcopy(mgras)
    # remove candidates with no vacant land ( 23002 to 8802)
    candidates = generic_filter(candidates, [mgra_labels.VACANT_ACRES])
    candidates = trim_columns(candidates)
    # for each mgra that has redev add candidates with each redev?
    redev_candidates = make_redev_candidates(mgras)
    print(redev_candidates.columns)
    print(len(redev_candidates))
    # candidates = pandas.merge(candidates, redev_candidates)
    # prep demand
    labels_demands = []
    for product_type_labels in all_product_type_labels():
        labels_demands.append((
            product_type_labels,
            (0, product_type_labels.units_per_year_parameter())
        ))

    progress_bar = tqdm(total=sum_demand(labels_demands))
    progress_bar.set_description(
        'allocating units by alternating through each product type')
    # select one build candidate at a time for each product type
    while demands_unsatisfied(labels_demands):
        for index, (labels, demand) in enumerate(labels_demands):
            if demand_unsatisfied(demand):
                mgras, built_demand = choose_candidate(
                    candidates,
                    mgras, labels, demand[1] - demand[0]
                )
                labels_demands[index] = (
                    labels, (demand[0] + built_demand, demand[1]))
                progress_bar.update(built_demand)
        random.shuffle(labels_demands)

    progress_bar.close()
    return mgras
