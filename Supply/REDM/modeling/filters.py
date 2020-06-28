import logging
import numpy

import utils.config as config

from utils.constants import product_type_price, LAND_COST_PER_ACRE, \
    VACANT_ACRES, CONSTRUCTION_COST_POSTFIX, OFFICE, COMMERCIAL, INDUSTRIAL, \
    MAX_VACANT_UNITS_POSTFIX

from utils.converter import x_per_acre_to_x_per_square_foot

# from utils.analysis import count_zeros


def filter_all(mgra_dataframe):
    '''
    performs any filtering that applies to all product types;
    eg. filter_vacant_land removes MGRA's with no land available to build on
    '''
    return filter_vacant_land(mgra_dataframe)


def filter_vacant_land(mgra_dataframe):
    return mgra_dataframe[mgra_dataframe[VACANT_ACRES] > 0]


def filter_product_type(mgra, product_type_vacant_key, acreage_per_unit):
    # must have space available
    return mgra[mgra[product_type_vacant_key] > acreage_per_unit * 1.2]


def filter_by_vacancy(mgra_dataframe, product_type, total_units_column,
                      occupied_units_column, target_vacancy_rate=None):
    if target_vacancy_rate is None:
        target_vacancy_rate = config.parameters[product_type +
                                                '_target_vacancy_rate']

    # maximum new units can be below zero if mgra is already over target
    # vacancy rate since vacancy = (total_units - occupied_units) / total_units
    # find max_units for a target_vacancy with some algebra:
    # max_units = -(occupied/(target_vacancy - 1))
    max_units = numpy.floor(
        -1*((mgra_dataframe[occupied_units_column]) /
            (target_vacancy_rate - 1))
    )
    max_new_units = max_units - mgra_dataframe[total_units_column]

    # check edge case; if there are few units built (eg. < 50 for single
    # family) we should build even when it causes a high vacancy rate
    max_vacant_units = config.parameters[product_type +
                                         MAX_VACANT_UNITS_POSTFIX]
    # this allows for up to max_vacant_units*2 - 1 units to be built before any
    # are occupied
    max_new_units[mgra_dataframe[total_units_column]
                  < max_vacant_units] = max_vacant_units

    # return the MGRA's that can add more than 0 units to meet
    # the target vacancy rate
    filtered = mgra_dataframe[max_new_units > 0]
    # also return max_new_units to use for weighting, but also remove
    # the low values to keep the frame and weighting series the same size
    max_new_units = max_new_units[max_new_units > 0]
    return filtered, max_new_units


# def profitable(revenue, price):
#     truth_values = numpy.where(revenue <= price, True, False)
#     # pass even with no price data
#     truth_values = numpy.where(price == 0, True, truth_values)
#     return truth_values


def filter_by_profitability(mgra_dataframe, product_type, vacancy_caps):
    # find total expected costs
    construction_cost = config.parameters[product_type +
                                          CONSTRUCTION_COST_POSTFIX]
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

    # find expected revenue
    if product_type == OFFICE or product_type == COMMERCIAL or \
            product_type == INDUSTRIAL:
        revenue = config.parameters[product_type + '_average_price']
    else:
        revenue = mgra_dataframe[product_type_price(product_type)]

    # debug info
    # uncomment to save frame to file
    # save_to_file(revenue, 'test_data/output', 'revenue ' + product_type)
    # logging.debug(
    #     'rows with missing data: {}/{}'.format(
    #         count_zeros(revenue), len(revenue))
    # )

    profit = revenue - amortized_costs
    logging.debug('mean profit: {}'.format(profit.mean()))
    profitability_criteria = (revenue >= amortized_minimum) | (revenue == 0)
    mgra_dataframe = mgra_dataframe[profitability_criteria]
    vacany_caps = vacancy_caps[profitability_criteria]
    profit = profit[profitability_criteria]
    return mgra_dataframe, vacany_caps, profit


# possible redev filter
