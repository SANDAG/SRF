import numpy

import utils.config as config

from utils.constants import product_type_price, LAND_COST_PER_ACRE, \
    VACANT_ACRES, CONSTRUCTION_COST_POSTFIX

from utils.converter import x_per_acre_to_x_per_square_foot


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


def filter_by_vacancy(mgra_dataframe, total_units_column,
                      occupied_units_column, target_vacancy_rate=None):
    if target_vacancy_rate is None:
        target_vacancy_rate = config.parameters['target_vacancy_rate']

    # maximum new units can be below zero if mgra is already over target
    # vacancy rate since vacancy = (total_units - occupied_units) / total_units
    # find max_units for a target_vacancy with some algebra:
    # max_units = -(occupied/(target_vacancy - 1))
    max_units = numpy.floor(
        -1*((mgra_dataframe[occupied_units_column]) /
            (target_vacancy_rate - 1))
    )
    max_new_units = max_units - mgra_dataframe[total_units_column]

    # check edge case; if there are few units built (< 50),
    # we should build even when it causes a high vacancy rate
    # FIXME: this allows for up to 99 units to be built before any are occupied
    max_new_units = numpy.where(
        mgra_dataframe[total_units_column] < 50, 50, max_new_units)

    # return the MGRA's that can add more than 0 units to meet
    # the target vacancy rate
    filtered = mgra_dataframe[max_new_units > 0]

    # also return max_new_units to use for weighting, but we need to remove
    # the low values as well to keep the return structures the same size
    max_new_units = numpy.delete(max_new_units, numpy.where(max_new_units < 1))

    # TODO: remove rows from max_new_units to be the same size as filtered
    return filtered, max_new_units


def filter_by_profitability(mgra_dataframe, product_type):
    construction_cost = config.parameters[product_type +
                                          CONSTRUCTION_COST_POSTFIX]
    price_column = product_type_price(product_type)
    land_cost_per_acre = mgra_dataframe[LAND_COST_PER_ACRE]
    profit_multiplier = config.parameters['profit_multiplier']
    land_cost_per_square_foot = x_per_acre_to_x_per_square_foot(
        land_cost_per_acre)
    minimum_revenue = (construction_cost +
                       land_cost_per_square_foot) * profit_multiplier
    profit = mgra_dataframe[price_column] - \
        (construction_cost + land_cost_per_square_foot)
    print(profit)
    return mgra_dataframe[minimum_revenue <= mgra_dataframe[price_column]]


# possible redev filter
