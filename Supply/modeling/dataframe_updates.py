import logging
import pandas

from utils.access_labels import mgra_labels, land_origin_labels


def add_to_columns(mgras, selected_ID, value, columns):
    '''
        value: number to add to the current values of columns
        columns: list of column labels
    '''
    if columns:
        mgras.loc[mgras[mgra_labels.MGRA] == selected_ID, columns] += value


def reallocate_units(mgras, selected_ID, count, from_columns, to_columns):
    '''
        moves `count` units from `from_columns` to `to_columns` at the row in
        `mgras` corresponding to the mgra id `selected_ID`
        updates the `mgras` dataframe in place
    '''
    add_to_columns(mgras, selected_ID, count, to_columns)
    # subtract from these columns
    add_to_columns(mgras, selected_ID, -1 * count, from_columns)


def update_acreage(mgras, selected_ID, new_acreage,
                   product_type_developed_key, product_type_vacant_key):
    # used for development on vacant land only
    reallocate_units(mgras, selected_ID, new_acreage,
                     from_columns=[
                         product_type_vacant_key,
                         mgra_labels.VACANT_ACRES
                     ],
                     to_columns=[
                         product_type_developed_key,
                         mgra_labels.DEVELOPED_ACRES
                     ])


def candidate_development_type(candidate, product_type_labels):
    '''
        find the land development label that corresponds to a non-NaN value
        each candidate is created with only one non-NaN land origin value
    '''
    possible_labels = land_origin_labels.applicable_labels_for(
        product_type_labels)
    for label in possible_labels:
        if pandas.notnull(candidate[label]).item():
            return label
    return None  # reaching this would signify a bug


def update_units(mgras, selected_ID, units_to_build, product_type_labels):
    columns_expecting_units = []
    columns_expecting_units.append(product_type_labels.total_units)
    if product_type_labels.is_residential():
        columns_expecting_units.append(mgra_labels.HOUSING_UNITS)
    else:  # product type is non-residential
        columns_expecting_units.append(mgra_labels.TOTAL_JOB_SPACES)
    add_to_columns(mgras, selected_ID, units_to_build,
                   columns_expecting_units)


def simple_update(mgras, selected_ID, units_to_build, product_type_labels):
    # used to maintain compatibility with the scheduled development module
    acreage_per_unit = product_type_labels.land_use_per_unit_parameter()
    new_acreage = acreage_per_unit * units_to_build
    update_acreage(mgras, selected_ID,
                   new_acreage,
                   product_type_labels.developed_acres,
                   product_type_labels.vacant_acres)

    square_feet_to_build = product_type_labels.unit_sqft_parameter() * \
        units_to_build
    add_to_columns(mgras, selected_ID, square_feet_to_build,
                   product_type_labels.square_footage)

    update_units(mgras, selected_ID, units_to_build, product_type_labels)


def update_mgra(mgras, selected_candidate,
                units_to_build, product_type_labels,
                scheduled_development=True):
    # let scheduled development pass through
    if scheduled_development:
        simple_update(mgras, selected_candidate,
                      units_to_build, product_type_labels)
        return

    selected_ID = selected_candidate[mgra_labels.MGRA].iloc[0]

    development_label = candidate_development_type(
        selected_candidate, product_type_labels)
    logging.debug('building {} {} units as {} on MGRA #{}'.format(
        units_to_build, product_type_labels.product_type,
        development_label, selected_ID))

    origin_type = land_origin_labels.label_type(development_label)
    origin_labels = land_origin_labels.get_origin(development_label)

    # Update acreages
    acreage_per_unit = product_type_labels.land_use_per_unit_parameter()
    new_acreage = acreage_per_unit * units_to_build
    if origin_type.vacant:
        update_acreage(mgras, selected_ID,
                       new_acreage,
                       product_type_labels.developed_acres,
                       product_type_labels.vacant_acres)
    elif origin_type.redev:
        # redevelopment should reallocate from the actual origin
        if origin_labels is None:
            origin_column_input = []
        else:
            origin_column_input = [origin_labels.developed_acres]
        reallocate_units(mgras, selected_ID, new_acreage,
                         from_columns=origin_column_input, to_columns=[
                             product_type_labels.developed_acres])
    # infill should only subtract from itself, redev also subtracts from itself
    if origin_type.redev or origin_type.infill:
        add_to_columns(mgras, selected_ID, -1 * new_acreage, development_label)

    # Update square footages
    # all three origin types increase square footage
    square_feet_to_build = product_type_labels.unit_sqft_parameter() * \
        units_to_build
    add_to_columns(mgras, selected_ID, square_feet_to_build,
                   product_type_labels.square_footage)
    if origin_type.redev and origin_labels is not None:
        # redevelopment should also subtract square footage from its origin
        # if it is being tracked
        add_to_columns(mgras, selected_ID, -1 *
                       square_feet_to_build, origin_labels.square_footage)

    # Update unit counts
    update_units(mgras, selected_ID, units_to_build, product_type_labels)
    # redeveloping should also subtract units from the original land use
    if origin_type.redev and origin_labels is not None:
        units_to_subtract = -1 * units_to_build
        update_units(mgras, selected_ID, units_to_subtract, origin_labels)
        return (origin_labels, units_to_subtract)
    return None
