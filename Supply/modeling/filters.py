import logging
import numpy

import utils.config as config

from utils.constants import LAND_COST_PER_ACRE
from utils.converter import x_per_acre_to_x_per_square_foot


def apply_filters(mgra_dataframe, product_type_labels, acreage_per_unit):
    '''
    applies each filtering method on the data frame
    logs the number of mgra's left after removing poor candidates
    returns: the filtered frame, as well as series/frames for use as
        selection weights and/or for capping development
    '''
    filtered = filter_product_type(
        mgra_dataframe, product_type_labels.vacant_acres, acreage_per_unit)
    available_count = len(filtered)

    filtered, vacancy_caps = filter_by_vacancy(
        filtered, product_type_labels)
    non_vacant_count = len(filtered)

    filtered, vacancy_caps, profits = filter_by_profitability(
        filtered, product_type_labels, vacancy_caps)
    profitable_count = len(filtered)

    logging.debug(
        'filtered to {} profitable / {} non-vacant / {}'.format(
            profitable_count, non_vacant_count, available_count
        ) + ' MGRA\'s with space available')

    return filtered, vacancy_caps, profits


def filter_product_type(mgra, product_type_vacant_key, acreage_per_unit):
    # filter for MGRA's that have land available (vacant, redev or infill)
    # for building more units of that product type
    # ! boolean should be true if there is vacant, redev, or infill available
    return mgra[mgra[product_type_vacant_key] > acreage_per_unit * 1.2]


def filter_by_vacancy(mgra_dataframe, product_type_labels,
                      target_vacancy_rate=None):
    total_units_column = mgra_dataframe[product_type_labels.total_units]
    occupied_units_column = mgra_dataframe[product_type_labels.occupied_units]
    if target_vacancy_rate is None:
        target_vacancy_rate = \
            product_type_labels.target_vacancy_rate_parameter()

    # maximum new units can be below zero if mgra is already over target
    # vacancy rate since vacancy = (total_units - occupied_units) / total_units
    # find max_units for a target_vacancy with some algebra:
    # max_units = -(occupied/(target_vacancy - 1))
    max_units = numpy.floor(
        -1*((occupied_units_column) /
            (target_vacancy_rate - 1))
    )
    max_new_units = max_units - total_units_column

    # check edge case; if there are few units built (eg. < 50 for single
    # family) we should build even when it causes a high vacancy rate
    max_vacant_units = product_type_labels.max_vacant_units_parameter()
    # this allows for up to max_vacant_units*2 - 1 units to be built before any
    # are occupied
    max_new_units[total_units_column
                  < max_vacant_units] = max_vacant_units

    # return the MGRA's that can add more than 0 units to meet
    # the target vacancy rate
    filtered = mgra_dataframe[max_new_units > 0]
    # also return max_new_units to use for weighting, but also remove
    # the low values to keep the frame and weighting series the same length
    max_new_units = max_new_units[max_new_units > 0]
    return filtered, max_new_units


def filter_by_profitability(mgra_dataframe, product_type_labels, vacancy_caps):
    """
        returns:
            - mgra_dataframe: the input dataframe with mgra's with no
            profitable land removed.
            - profitability: a dataframe with three columns corresponding to
            greenfield, infill, and redevelopment profitability for that mgra.
    """
    # TODO: find the cost for each development type
    # find total expected costs
    construction_cost = product_type_labels.construction_cost_parameter()
    land_cost_per_acre = mgra_dataframe[LAND_COST_PER_ACRE]
    land_cost_per_square_foot = x_per_acre_to_x_per_square_foot(
        land_cost_per_acre)
    expected_costs = construction_cost + land_cost_per_square_foot

    # find minimum returns for viable MGRA's
    profit_multiplier = config.parameters['profit_multiplier']
    minimum_revenue = expected_costs * profit_multiplier
    years = config.parameters['amortization_years']
    amortized_minimum = minimum_revenue / \
        years
    amortized_costs = expected_costs / years

    # get expected revenue
    revenue = mgra_dataframe[product_type_labels.price]

    profit = revenue - amortized_costs
    profitability_criteria = (revenue >= amortized_minimum) | (revenue == 0)

    for i in range(10):
        print(profit.sample(n=1).item())

    mgra_dataframe = mgra_dataframe[profitability_criteria]
    vacancy_caps = vacancy_caps[profitability_criteria]
    profit = profit[profitability_criteria]
    return mgra_dataframe, vacancy_caps, profit
