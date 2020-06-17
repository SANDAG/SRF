import logging

import utils.config as config
from utils.converter import square_feet_to_acres
from utils.constants import development_constants, MGRA, HOUSING_UNITS, \
    OFFICE, COMMERCIAL, INDUSTRIAL, SINGLE_FAMILY, MULTI_FAMILY, \
    DEVELOPED_ACRES, VACANT_ACRES, \
    SINGLE_FAMILY_HOUSING_UNITS, MULTI_FAMILY_HOUSING_UNITS
from modeling.filters import filter_product_type, filter_by_vacancy, \
    filter_by_profitability


def update_mgra(mgras, selected_ID, acreage_per_unit,
                product_type_developed_land, product_type_vacant_land,
                new_units, product_type_units):
    mgras = update_acreage(mgras, selected_ID,
                           acreage_per_unit * new_units,
                           product_type_developed_land,
                           product_type_vacant_land)
    # TODO: also update non-residential units once data is available
    if product_type_units == SINGLE_FAMILY_HOUSING_UNITS or \
            product_type_units == MULTI_FAMILY_HOUSING_UNITS:
        mgras = update_housing(
            mgras, selected_ID, new_units,
            product_type_units)
    return mgras


def update_acreage(
    mgras, selected_ID, new_acreage,
    product_type_developed_key, product_type_vacant_key
):
    # TODO: ensure that no other acreage updates are needed
    mgras.loc[mgras[MGRA] == selected_ID, [
        product_type_developed_key, DEVELOPED_ACRES]] += new_acreage
    mgras.loc[mgras[MGRA] == selected_ID, [
        product_type_vacant_key, VACANT_ACRES]] -= new_acreage
    return mgras


def update_housing(mgras, selected_ID, new_units, product_type_units):
    mgras.loc[mgras[MGRA] == selected_ID, [
        HOUSING_UNITS, product_type_units]] += new_units
    return mgras


def parameters_for_product_type(product_type):
    # FIXME: this is goofy
    if product_type.__contains__('family'):
        floor_space = square_feet_to_acres(
            config.parameters[product_type + '_minimum_unit_size'])
    else:
        floor_space = square_feet_to_acres(
            config.parameters[product_type + '_square_feet_per_job']
        )
    return config.parameters[product_type + '_units_per_year'], floor_space


def profitable_units(mgra, product_type_developed_key, product_type_vacant_key,
                     area_per_unit, max_units):
    # determine how many units to build

    # TODO: use profitability and vacancy filter values to determine
    # the number of units to build.
    # this placeholder allows for building 95% of the vacant space
    available_units = mgra[product_type_vacant_key].values.item() * \
        0.95 // area_per_unit

    # only build up to maximum units
    if available_units > max_units:
        return max_units
    else:
        return available_units


def develop_product_type(mgras, product_type, progress):
    if progress is not None:
        progress.set_description('developing {}'.format(product_type))

    new_units_to_build, acreage_per_unit = parameters_for_product_type(
        product_type)

    product_type_developed_key, product_type_vacant_key, \
        total_units_key, occupied_units_key = development_constants(
            product_type)

    built_units = 0
    while built_units < new_units_to_build:
        # filter for MGRA's that have vacant land available for more units
        filtered = filter_product_type(
            mgras, product_type_vacant_key, acreage_per_unit)
        available_count = len(filtered)

        # FIXME: remove check once non-residential occupancy data is
        # available
        if total_units_key is not None and occupied_units_key is not None:
            filtered, _ = filter_by_vacancy(
                filtered, total_units_key, occupied_units_key)
        non_vacant_count = len(filtered)

        filtered, _ = filter_by_profitability(filtered, product_type)
        profitable_count = len(filtered)

        logging.debug(
            'filtered to {} profitable / {} non-vacant / {}'.format(
                profitable_count, non_vacant_count, available_count
            ) + ' MGRA\'s with space available')
        if len(filtered) < 1:
            print(
                'out of usable mgras for product type {}'.format(product_type)
            )
            print('evaluate filtering methods and demand parameters')
            print('exiting')
            return None, progress
        # TODO: add weighting (use sample(weights=))
        # (profitability, proximity to developed mgra's, vacancy)
        selected_row = filtered.sample(n=1)
        selected_ID = selected_row[MGRA].iloc[0]
        max_units = new_units_to_build - built_units
        buildable_count = profitable_units(
            selected_row, product_type_developed_key,
            product_type_vacant_key, acreage_per_unit, max_units
        )

        built_units += buildable_count

        logging.debug('building {} units on MGRA #{}'.format(
            buildable_count, selected_ID))

        # develop buildable_count units by updating the MGRA in the dataframe
        mgras = update_mgra(mgras, selected_ID, acreage_per_unit,
                            product_type_developed_key,
                            product_type_vacant_key, buildable_count,
                            total_units_key)

    if progress is not None:
        progress.update()
    return mgras, progress


def develop(mgras, progress=None):
    """
    Arguments
        mgras:
            A pandas dataframe of mgra's that will be updated with new values
            based on demand inputs found in parameters.yaml
    Returns:
        a pandas dataframe with selected MGRA's updated
    """
    product_types = [SINGLE_FAMILY, MULTI_FAMILY,
                     COMMERCIAL, OFFICE, INDUSTRIAL]
    for product_type in product_types:
        mgras, progress = develop_product_type(
            mgras, product_type, progress)
        if mgras is None:
            return mgras, progress

    # tests don't use a progress bar
    if progress is not None:
        return mgras, progress
    else:
        return mgras
