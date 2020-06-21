from modeling.filters import filter_product_type, filter_by_vacancy, \
    filter_by_profitability
import logging

import utils.config as config
from utils.converter import square_feet_to_acres
from utils.constants import development_constants, \
    non_residential_vacant_units, MGRA, HOUSING_UNITS, \
    AVERAGE_UNIT_SQFT_POSTFIX, UNITS_PER_YEAR_POSTFIX, \
    OFFICE, COMMERCIAL, INDUSTRIAL, SINGLE_FAMILY, MULTI_FAMILY, \
    DEVELOPED_ACRES, VACANT_ACRES, \
    SINGLE_FAMILY_HOUSING_UNITS, MULTI_FAMILY_HOUSING_UNITS


def update_acreage(mgras, selected_ID, new_acreage,
                   product_type_developed_key, product_type_vacant_key):
    mgras.loc[mgras[MGRA] == selected_ID, [
        product_type_developed_key, DEVELOPED_ACRES]] += new_acreage
    mgras.loc[mgras[MGRA] == selected_ID, [
        product_type_vacant_key, VACANT_ACRES]] -= new_acreage
    return mgras


def add_to_columns(mgras, selected_ID, value, columns):
    '''
        columns: list of column labels
        value: number to add to the current values of columns
    '''
    mgras.loc[mgras[MGRA] == selected_ID, columns] += value
    return mgras


def update_mgra(mgras, selected_ID, acreage_per_unit,
                product_type_developed_land, product_type_vacant_land,
                new_units, product_type_units):
    mgras = update_acreage(mgras, selected_ID,
                           acreage_per_unit * new_units,
                           product_type_developed_land,
                           product_type_vacant_land)
    columns_needing_new_units = [product_type_units]

    if product_type_units == SINGLE_FAMILY_HOUSING_UNITS or \
            product_type_units == MULTI_FAMILY_HOUSING_UNITS:
        columns_needing_new_units.append(HOUSING_UNITS)
    else:
        columns_needing_new_units.append(
            non_residential_vacant_units(product_type_units))
    return add_to_columns(mgras, selected_ID, new_units,
                          columns_needing_new_units)


def parameters_for_product_type(product_type):
    floor_space = square_feet_to_acres(
        config.parameters[product_type + AVERAGE_UNIT_SQFT_POSTFIX])
    # land_use =
    return config.parameters[product_type + UNITS_PER_YEAR_POSTFIX], \
        floor_space


def buildable_units(mgra, product_type_developed_key, product_type_vacant_key,
                    area_per_unit, max_units, vacancy_caps):
    # determine max units to build
    vacancy_cap = vacancy_caps[mgra.index]

    # TODO: also use profitability filter value for this mgra to determine
    # the number of profitable units to build.

    # only build up to 95% of the vacant space
    available_units_by_land = mgra[product_type_vacant_key].values.item() * \
        0.95 // area_per_unit

    # this is a sanity check, no development should be larger than this number
    largest_development = config.parameters['largest_development_size']
    return int(min(max_units, largest_development,
                   vacancy_cap, available_units_by_land))


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
        max_units = new_units_to_build - built_units

        # Filter
        # filter for MGRA's that have vacant land available for more units
        filtered = filter_product_type(
            mgras, product_type_vacant_key, acreage_per_unit)
        available_count = len(filtered)

        filtered, vacancy_caps = filter_by_vacancy(
            filtered, product_type, total_units_key, occupied_units_key)
        non_vacant_count = len(filtered)

        filtered, _ = filter_by_profitability(filtered, product_type)
        profitable_count = len(filtered)

        logging.debug(
            'filtered to {} profitable / {} non-vacant / {}'.format(
                profitable_count, non_vacant_count, available_count
            ) + ' MGRA\'s with space available')

        if len(filtered) < 1:
            print('out of usable mgras for product type {}'.format(
                product_type))
            print('evaluate filtering methods\nexiting')
            return None, progress
        # reset the index to simplify comparisons with weighting arrays
        # output mgras dataframe is updated using mgra_id's instead of indices
        filtered = filtered.reset_index()

        # Sample
        # TODO: add weighting (use sample(weights=))
        # (profitability, vacancy, other geographic weights)
        selected_row = filtered.sample(n=1)
        selected_ID = selected_row[MGRA].iloc[0]

        buildable_count = buildable_units(
            selected_row, product_type_developed_key,
            product_type_vacant_key, acreage_per_unit, max_units, vacancy_caps
        )
        built_units += buildable_count

        logging.debug('building {} {} units on MGRA #{}'.format(
            buildable_count, product_type, selected_ID))

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
