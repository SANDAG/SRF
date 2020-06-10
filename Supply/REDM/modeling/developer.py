import utils.config as config
from utils.converter import square_feet_to_acres
from utils.constants import MGRA, HOUSING_UNITS, \
    DEVELOPED_ACRES, VACANT_ACRES, \
    SINGLE_FAMILY_HOUSING_UNITS, MULTI_FAMILY_HOUSING_UNITS, \
    SINGLE_FAMILY_DEVELOPED_ACRES, SINGLE_FAMILY_VACANT_ACRES, \
    MULTI_FAMILY_DEVELOPED_ACRES, MULTI_FAMILY_VACANT_ACRES, \
    OFFICE_DEVELOPED_ACRES, OFFICE_VACANT_ACRES, \
    COMMERCIAL_DEVELOPED_ACRES, COMMERCIAL_VACANT_ACRES, \
    INDUSTRIAL_DEVELOPED_ACRES, INDUSTRIAL_VACANT_ACRES

# product types - must match data labels
SINGLE_FAMILY = 'single_family'
MULTI_FAMILY = 'multi_family'

INDUSTRIAL = 'industrial'
COMMERCIAL = 'commercial'
OFFICE = 'office'


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
    if product_type.__contains__('family'):
        floor_space = square_feet_to_acres(
            config.parameters[product_type + '_minimum_unit_size'])
    else:
        floor_space = square_feet_to_acres(
            config.parameters[product_type + '_square_feet_per_job']
        )
    return config.parameters['new_units_' + product_type], floor_space


def constants_for_product_type(product_type):
    if product_type == OFFICE:
        return OFFICE_DEVELOPED_ACRES, OFFICE_VACANT_ACRES
    elif product_type == COMMERCIAL:
        return COMMERCIAL_DEVELOPED_ACRES, COMMERCIAL_VACANT_ACRES
    elif product_type == INDUSTRIAL:
        return INDUSTRIAL_DEVELOPED_ACRES, INDUSTRIAL_VACANT_ACRES
    elif product_type == SINGLE_FAMILY:
        return SINGLE_FAMILY_DEVELOPED_ACRES, SINGLE_FAMILY_VACANT_ACRES
    elif product_type == MULTI_FAMILY:
        return MULTI_FAMILY_DEVELOPED_ACRES, MULTI_FAMILY_VACANT_ACRES


def profitable_units(mgra, product_type_developed_key, product_type_vacant_key,
                     area_per_unit, max_units):
    # determine how many units to build

    # this placeholder allows for building 90% of the vacant space
    # available_units = mgra[product_type_vacant_key].values.item() * \
    #     0.9 // area_per_unit

    # alternatively, build up to 90% of developed + vacant
    # 90% being a placeholder for how dense of construction would be profitable
    developed_space = mgra[product_type_developed_key].values.item()

    total_space = developed_space + mgra[product_type_vacant_key]
    profitable_space = 0.9 * total_space.values.item()
    if profitable_space > developed_space:
        available_area = profitable_space - developed_space
        available_units = available_area // area_per_unit
    else:
        # there isn't any profitable space, but let's just build one unit
        # anyway
        available_units = 1

    # if more than max, return max
    if available_units > max_units:
        return max_units
    else:
        return available_units


def develop_product_type(mgras, filtered, product_type, progress):
    if progress is not None:
        progress.set_description('developing {}'.format(product_type))

    new_units_to_build, acreage_per_unit = parameters_for_product_type(
        product_type)
    product_type_developed_key, product_type_vacant_key = \
        constants_for_product_type(product_type)

    built_units = 0
    while built_units < new_units_to_build:

        # TODO select mgras that have enough acreage per unit for development
        # to be profitable
        mgras_of_type = filtered[filtered[product_type_vacant_key]
                                 > acreage_per_unit * 1.2]

        # TODO: add weighting (use sample(weights=))
        # (profitability, proximity to developed mgra's, vacancy)
        selected_row = mgras_of_type.sample(n=1)
        selected_ID = selected_row[MGRA].iloc[0]
        max_units = new_units_to_build - built_units
        buildable_count = profitable_units(
            selected_row, product_type_developed_key,
            product_type_vacant_key, acreage_per_unit, max_units
        )

        built_units += buildable_count
        # print(buildable_count)
        mgras = update_acreage(mgras, selected_ID,
                               acreage_per_unit * buildable_count,
                               product_type_developed_key,
                               product_type_vacant_key)

        if product_type == SINGLE_FAMILY:
            mgras = update_housing(
                mgras, selected_ID, buildable_count,
                SINGLE_FAMILY_HOUSING_UNITS)
        elif product_type == MULTI_FAMILY:
            mgras = update_housing(
                mgras, selected_ID, buildable_count,
                MULTI_FAMILY_HOUSING_UNITS)

        # Add any further updates to the mgra here

    if progress is not None:
        progress.update()
    return mgras, progress


def develop(mgras, filtered, progress=None):
    """
    Arguments
        mgras:
            A pandas dataframe of mgra's that will be updated with new values
            based on demand inputs found in parameters.yaml
        filtered:
            contains a selection of all MGRA's available to develop
    Returns:
        a pandas dataframe with selected MGRA's updated
    """

    product_types = [SINGLE_FAMILY, MULTI_FAMILY,
                     COMMERCIAL, OFFICE, INDUSTRIAL]
    for product_type in product_types:
        mgras, progress = develop_product_type(
            mgras, filtered, product_type, progress)

    if progress is not None:
        return mgras, progress
    else:
        return mgras
