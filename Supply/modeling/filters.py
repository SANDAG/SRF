import logging
import numpy
import pandas

import utils.config as config
from utils.access_labels import mgra_labels
from utils.converter import x_per_acre_to_x_per_square_foot


def generic_filter(dataframe, columns, filter_nans=True, filter_zeros=True):
    '''
        columns: a list containing the columns to be evaluated
        returns: dataframe with the rows removed that have NAN's or zeros in
        any of the specified columns
    '''
    for column in columns:
        if filter_zeros:
            dataframe = dataframe[dataframe[column] != 0]
        if filter_nans:
            dataframe = dataframe[pandas.notnull(dataframe[column])]
    return dataframe


def apply_filters(mgra_dataframe, product_type_labels):
    '''
    applies each filtering method on the data frame
    logs the number of mgra's left after removing poor candidates
    returns: the filtered frame, as well as series/frames for use as
        selection weights and/or for capping development
    '''

    filtered, land_caps = filter_product_type(
        mgra_dataframe, product_type_labels)
    available_count = len(filtered)

    filtered, max_units = filter_by_vacancy(
        filtered, product_type_labels, land_caps=land_caps)
    non_vacant_count = len(filtered)

    filtered, max_units, profits = filter_by_profitability(
        filtered, product_type_labels, max_units)
    profitable_count = len(filtered)

    logging.debug(
        'filtered to {} profitable / {} non-vacant / {}'.format(
            profitable_count, non_vacant_count, available_count
        ) + ' MGRA\'s with space available')

    return filtered, max_units, profits


def filter_product_type(mgra_dataframe, product_type_labels):
    # filter for MGRA's that have land available (vacant, redev or infill)
    # for building more units of that product type
    # ! boolean should be true if there is vacant, redev, or infill available
    acreage_per_unit = product_type_labels.land_use_per_unit_parameter()
    MINIMUM_UNITS = 5
    vacant_land = mgra_dataframe[product_type_labels.vacant_acres]
    units_available = vacant_land // acreage_per_unit

    # pseudo code for also checking all applicable redev and infill columns
    # redev_units_available = \
    #    get_max_of_redev_and_infill_options() // acreage_per_unit
    # units_available = max(units_available, redev_units_available)

    # also check residential capacity values here
    if product_type_labels.is_residential():
        remaining_capacity = mgra_dataframe[product_type_labels.capacity] - \
            mgra_dataframe[product_type_labels.total_units]
        units_available = units_available[
            units_available > remaining_capacity] = remaining_capacity

    criteria = (units_available > MINIMUM_UNITS)
    return mgra_dataframe[criteria], units_available[criteria]


def filter_by_vacancy(mgra_dataframe, product_type_labels, land_caps=None,
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
    criteria = (max_new_units > 0)
    filtered = mgra_dataframe[criteria]

    # also return max_new_units to use for weighting, but also remove
    # the low values to keep the frame and weighting series the same length
    if land_caps is not None:
        # if land_caps is given as an input, return the minimum of each
        # corresponding index
        land_caps = land_caps[criteria]
        # max_new_units needs to be shortened last
        max_new_units = max_new_units[criteria]
        max_new_units = pandas.concat(
            [land_caps, max_new_units], axis=1).min(axis=1)
    else:
        max_new_units = max_new_units[criteria]
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
    land_cost_per_acre = mgra_dataframe[mgra_labels.LAND_COST_PER_ACRE]
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

    mgra_dataframe = mgra_dataframe[profitability_criteria]
    vacancy_caps = vacancy_caps[profitability_criteria]
    profit_margins = profit[profitability_criteria] / \
        revenue[profitability_criteria]

    return mgra_dataframe, vacancy_caps, profit_margins
