from numpy import floor

import utils.config as config

from utils.constants import LAND_COST_PER_ACRE, VACANT_ACRES, \
    SINGLE_FAMILY_RENT, MULTI_FAMILY_RENT, INDUSTRIAL_RENT, \
    OFFICE_RENT, COMMERCIAL_RENT, OFFICE, COMMERCIAL, INDUSTRIAL, \
    SINGLE_FAMILY, MULTI_FAMILY, CONSTRUCTION_COST_POSTFIX

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

    max_new_units = max_new_units_to_meet_vacancy(
        mgra_dataframe, total_units_column, occupied_units_column,
        target_vacancy_rate
    )
    # return the MGRA's that can add more units to meet the target vacancy rate
    # We may want to use a number larger than zero
    filtered = mgra_dataframe[max_new_units > 0]

    # also return max_new_units to use for weighting
    # TODO: remove rows from max_new_units to be the same size as filtered
    return filtered, max_new_units


def max_new_units_to_meet_vacancy(mgra, total_units_column,
                                  occupied_units_column, target_vacancy_rate):
    # can be below zero if mgra is already over target vacancy rate
    # since vacancy = (total_units - occupied_units) / total_units
    # find max_units for a target_vacancy with some algebra:
    # max_units = -(occupied/(target_vacancy - 1))
    max_units = floor(
        -1*((mgra[occupied_units_column]) / (target_vacancy_rate - 1))
    )
    max_new_units = max_units - mgra[total_units_column]

    return max_new_units


def get_construction_cost(product_type):
    return config.parameters[product_type + CONSTRUCTION_COST_POSTFIX]


def profitability_constants(product_type):
    '''
        Returns the column label for rents/prices and the construction cost
        parameter for the product type argument
    '''
    construction_cost = get_construction_cost(product_type)
    if product_type == SINGLE_FAMILY:
        return SINGLE_FAMILY_RENT, construction_cost
    elif product_type == MULTI_FAMILY:
        return MULTI_FAMILY_RENT, construction_cost
    elif product_type == OFFICE:
        return OFFICE_RENT, construction_cost
    elif product_type == INDUSTRIAL:
        return INDUSTRIAL_RENT, construction_cost
    elif product_type == COMMERCIAL:
        return COMMERCIAL_RENT, construction_cost


def filter_by_profitability(mgra_dataframe, product_type):
    price_column, construction_cost = profitability_constants(product_type)
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
