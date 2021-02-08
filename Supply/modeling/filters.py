import logging
import numpy
import pandas

from utils.parameter_access import parameters
from utils.access_labels import mgra_labels, land_origin_labels
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
    return dataframe.copy()


def apply_filters(candidates, product_type_labels):
    '''
    applies each filtering method on the candidates
    logs the number of options left after removing poor candidates
    returns: the filtered frame, as well as series/frames for use as
        selection weights and/or for capping development
    '''
    filtered = filter_product_type(
        candidates, product_type_labels)
    available_count = len(filtered)

    filtered = filter_by_vacancy(
        filtered, product_type_labels)

    non_vacant_count = len(filtered)

    filtered = filter_by_profitability(
        filtered, product_type_labels)
    profitable_count = len(filtered)

    logging.debug(
        'filtered to {} profitable / {} non-vacant / {}'.format(
            profitable_count, non_vacant_count, available_count
        ) + ' MGRA\'s with space available')

    return filtered.copy()


def acreage_available(candidates, product_type_labels):
    '''
        returns a pandas series the same length as candidates,
        with entries made up of each candidate's land origin size
    '''
    possible_labels = land_origin_labels.applicable_labels_for(
        product_type_labels)
    acres_available = None
    for label in possible_labels:
        if acres_available is None:
            acres_available = candidates[label].copy()
        else:
            if label == product_type_labels.vacant_acres:
                other = candidates[[mgra_labels.VACANT_ACRES, label]].min(
                    axis=1)
            else:
                other = candidates[label]
            acres_available.where(pandas.notnull(
                acres_available), other=other, inplace=True)
    return acres_available.copy()


def filter_product_type(candidates, product_type_labels):
    # filter for MGRA's that have land available (vacant, redev or infill)
    # for building more units of that product type
    acreage_per_unit = product_type_labels.land_use_per_unit_parameter()

    # remove each candidate that doesn't have land allocated for the
    # product type
    # ! test acreage_available
    vacant_land = acreage_available(candidates, product_type_labels)
    units_available = vacant_land // acreage_per_unit

    # also check capacity values here
    if product_type_labels.is_residential():
        remaining_capacity = candidates[product_type_labels.capacity] - \
            candidates[product_type_labels.total_units]
        units_available = units_available[
            units_available > remaining_capacity] = remaining_capacity
    else:
        remaining_capacity = candidates[
            mgra_labels.CIVILIAN_EMPLOYMENT_CAPACITY
        ] - candidates[mgra_labels.TOTAL_JOB_SPACES]
        units_available = units_available[
            units_available > remaining_capacity] = remaining_capacity
    candidates['units_available'] = units_available

    return candidates[
        candidates['units_available'] > parameters['minimum_units']
    ].copy()


def filter_by_vacancy(mgra_dataframe, product_type_labels, land_caps=None,
                      target_vacancy_rate=None):
    # the vacancy filter is agnostic of original candidate land type.
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
    # use the column from filter_product_type, find min of those values and
    # these new ones.
    mgra_dataframe.loc[:, 'vacancy_cap'] = pandas.concat(
        [mgra_dataframe.units_available, max_new_units],
        axis=1
    ).min(axis=1)

    # return the MGRA's that can add more than 'minimum' units before meeting
    # the target vacancy rate
    return mgra_dataframe[
        mgra_dataframe['vacancy_cap'] > parameters['minimum_units']]


def get_series_for_label(mgra_dataframe, label, multiplier):
    # grab the column
    series = mgra_dataframe[label].copy()
    # set all non-null values equal to the multiplier
    series[pandas.notnull(series)] = multiplier
    return series


def construction_multiplier(mgra_dataframe, product_type_labels):
    '''
        returns: a pandas Series with multipliers determined by the land
        original type and parameters
    '''
    # start with vacant land, if the value was NaN, it should still be NaN
    series = get_series_for_label(
        mgra_dataframe, product_type_labels.vacant_acres,
        parameters['vacant_cost_multiplier'])

    infill_label = land_origin_labels.infill_label(product_type_labels)
    infill_series = get_series_for_label(
        mgra_dataframe, infill_label, parameters['infill_cost_multiplier'])
    # take infill series entries for all null entries
    series.where(pandas.notnull(series), other=infill_series, inplace=True)
    # now do the same for each redevelopment option
    redev_labels = land_origin_labels.redev_labels(product_type_labels)
    for label in redev_labels:
        redev_series = get_series_for_label(
            mgra_dataframe, label, parameters['redevelopment_cost_multiplier'])
        series.where(pandas.notnull(series), other=redev_series, inplace=True)

    # each value should be nonnull
    return series.copy()


def filter_by_profitability(candidates, product_type_labels):
    """
        returns:
            - candidates: the input dataframe with candidates's with no
            profitable land removed.
            - profitability: a dataframe with three columns corresponding to
            greenfield, infill, and redevelopment profitability for that mgra.
    """
    # find total expected costs
    construction_cost = product_type_labels.construction_cost_parameter()
    # multiplier will depend on each candidate's origin type
    construction_cost *= construction_multiplier(
        candidates, product_type_labels)
    land_cost_per_acre = candidates[mgra_labels.LAND_COST_PER_ACRE]
    land_cost_per_square_foot = x_per_acre_to_x_per_square_foot(
        land_cost_per_acre)
    expected_costs = construction_cost + land_cost_per_square_foot

    # find minimum returns for viable MGRA's
    profit_multiplier = parameters['profit_multiplier']
    minimum_revenue = expected_costs * profit_multiplier
    years = parameters['amortization_years']
    amortized_minimum = minimum_revenue / \
        years
    amortized_costs = expected_costs / years

    # get expected revenue
    revenue = candidates[product_type_labels.price]

    profit = revenue - amortized_costs

    profitability_criteria = revenue >= amortized_minimum

    candidates = candidates[profitability_criteria].copy()
    candidates.loc[:, 'profit_margin'] = profit[profitability_criteria] / \
        revenue[profitability_criteria]

    return candidates.copy()
