import logging
import pandas

from utils.access_labels import mgra_labels, land_origin_labels, \
    residential_labels
from utils.parameter_access import parameters
from utils.pandas_shortcuts import get_item


def add_to_columns(mgras, selected_ID, value, columns):
    '''
        value: number to add to the current values of columns
        columns: list of column labels
    '''
    if columns and mgras is not None:
        mgras.loc[mgras[mgra_labels.MGRA] == selected_ID, columns] += value


def add_to_columns_with_tracking(
        mgras, candidates, selected_ID, value, columns):
    '''
        a wrapper method for add_to_columns that calls add_to_columns twice,
        once for the mgra in mgras, and once for all of the candidates with
        the same mgra id, so that they can keep track of the changes that
        other candidates make on their mgra
    '''
    add_to_columns(mgras, selected_ID, value, columns)
    add_to_columns(candidates, selected_ID, value, columns)


def safely_subtract_from_columns(
        mgras, candidates, selected_ID, count, from_columns):
    '''
        subtracts count from columns, but also checks that each column
        remained above zero. (candidates are allowed to stay negative)
    '''
    add_to_columns_with_tracking(
        mgras, candidates, selected_ID, -1 * count, from_columns)
    for column in from_columns:
        if mgras.loc[
                mgras[mgra_labels.MGRA] == selected_ID, column
        ].item() < 0:
            logging.warning(
                'Attempted to make {} negative on MGRA {} '.format(
                    column, int(selected_ID)), + 'setting it to zero instead')
            mgras.loc[mgras[mgra_labels.MGRA] == selected_ID, column] = 0


def reallocate_units(mgras, candidates, selected_ID,
                     count, from_columns, to_columns):
    '''
        moves `count` units from `from_columns` to `to_columns` at the row in
        `mgras` corresponding to the mgra id `selected_ID`
        updates the `mgras` dataframe in place
    '''
    add_to_columns_with_tracking(
        mgras, candidates, selected_ID, count, to_columns)
    # subtract from these columns
    safely_subtract_from_columns(
        mgras, candidates, selected_ID, count, from_columns)


def update_acreage(mgras, selected_ID, new_acreage,
                   product_type_developed_key, product_type_vacant_key,
                   candidates=None):
    # used for development on vacant land only
    reallocate_units(mgras, candidates, selected_ID, new_acreage,
                     from_columns=[
                         product_type_vacant_key,
                         mgra_labels.VACANT_ACRES
                     ],
                     to_columns=[
                         product_type_developed_key,
                         mgra_labels.DEVELOPED_ACRES
                     ])
    if mgras.loc[mgras[mgra_labels.MGRA] == selected_ID,
                 mgra_labels.VACANT_ACRES].item() < 0:
        logging.error('removed too much vacant land')
        logging.error(mgras.loc[mgras[mgra_labels.MGRA] == selected_ID])


def candidate_development_type(candidate, product_type_labels):
    '''
        find the land development label that corresponds to a non-NaN value
        each candidate is created with only one non-NaN land origin value
    '''
    possible_labels = land_origin_labels.applicable_labels_for(
        product_type_labels)
    logging.debug('candidate check type: {}'.format(
        candidate[possible_labels]))
    for label in possible_labels:
        if pandas.notnull(candidate[label]).item():
            return label
    return None  # reaching this would signify a bug


def previous_proportion_in_units(
        mgra_row, proportion_label, current_units_label):
    return mgra_row[proportion_label] * mgra_row[current_units_label]


def update_proportion(
        frame, selected_ID, proportion_column, updated_proportion_units,
        total_units_after_update):
    if total_units_after_update == 0:
        return
    frame.loc[
        frame[mgra_labels.MGRA] == selected_ID, proportion_column
    ] = updated_proportion_units / total_units_after_update


def update_housing_ages(mgras, selected_ID, units_to_build,
                        product_type_labels):
    '''
    changes the mgras frame in place so that the proportion of new and old
    buildings for the product type are accurate based on the number of new
    units that will be added to the mgra
    '''
    # any additional units should be added to the proportion of new units
    # any negative units should be taken first from the 'old' category, then
    # the middle aged category
    # (all proportions need to be updated to maintain accuracy though)
    row = mgras.loc[mgras[mgra_labels.MGRA] == selected_ID, :]
    total_units_after_update = get_item(
        mgras, mgra_labels.MGRA, selected_ID,
        product_type_labels.total_units) + units_to_build
    previous_new_units = previous_proportion_in_units(
        row,
        product_type_labels.proportion_new,
        product_type_labels.total_units
    )
    previous_old_units = previous_proportion_in_units(
        row, product_type_labels.proportion_old,
        product_type_labels.total_units)

    if units_to_build >= 0:
        # add to proportion new
        new_units = previous_new_units + units_to_build
        old_units = previous_old_units
    else:
        new_units = previous_new_units
        # subtract (notice we already have negative units_to_build) from
        # proportion old
        old_units = previous_old_units + units_to_build

    if old_units.item() < 0:
        old_units = 0

    update_proportion(mgras, selected_ID, product_type_labels.proportion_new,
                      new_units, total_units_after_update)
    # update proportion old
    update_proportion(mgras, selected_ID, product_type_labels.proportion_old,
                      old_units, total_units_after_update)


def update_units(mgras, selected_ID, units_to_build, product_type_labels,
                 candidates=None):
    columns_expecting_units = []
    columns_expecting_units.append(product_type_labels.total_units)
    if product_type_labels.is_residential():
        columns_expecting_units.append(mgra_labels.HOUSING_UNITS)
        update_housing_ages(mgras, selected_ID,
                            units_to_build, product_type_labels)
    else:  # product type is non-residential
        columns_expecting_units.append(mgra_labels.TOTAL_JOB_SPACES)
    add_to_columns_with_tracking(
        mgras, candidates, selected_ID, units_to_build,
        columns_expecting_units)


def __change_in_proportion(current_proportion, proportion_range):
    return current_proportion / proportion_range


def increment_building_ages(mgras):
    '''
    Inputs: full mgra frame to be updated in place with the mean_new and
    mean_old values for the housing product types by 'aging out' one year's
    worth of buildings
    For example: if one mgra had 2% new buildings, new being defined as less
    than 20 years old, one year's worth (1/20) of those buildings should age
    out, updating the new buildings measurement for that mgra to 1.9%.
    The unit count for the product type will be used in determining the number
    of units to age out.
    Assumptions: This assumes that the buildings are equally distributed
    throughout the years
        - This should only be called once every time step, as opposed to the
        rest of the functions in dataframe_updates so far, which are invoked
        with each selected candidate.
    Returns: None, frame is updated in place
    '''
    for labels in residential_labels():
        # calculate the proportion of new housing
        # save in a temp variable to not change the calculations for
        # proportion old
        updated_proportion_new = mgras[labels.proportion_new] - \
            __change_in_proportion(
            mgras[labels.proportion_new], parameters['years_new'])
        # update the proportion of old housing
        middle_aged_proportion = 1.0 - \
            mgras[labels.proportion_new] - mgras[labels.proportion_old]
        middle_age_range = parameters['years_old'] - parameters['years_new']
        mgras[labels.proportion_old] += __change_in_proportion(
            middle_aged_proportion, middle_age_range
        )
        # now save the calculated proportion of new housing
        mgras[labels.proportion_new] = updated_proportion_new


def simple_update(mgras, selected_ID, units_to_build, product_type_labels):
    # used by the scheduled development module
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
                scheduled_development=True, candidates=None):
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
    logging.debug('acreage we are about to add: {}'.format(new_acreage))
    if origin_type.vacant:
        update_acreage(mgras, selected_ID,
                       new_acreage,
                       product_type_labels.developed_acres,
                       product_type_labels.vacant_acres, candidates=candidates)
    elif origin_type.redev:
        # redevelopment should reallocate from the actual origin
        if origin_labels is None:
            origin_column_input = []
        else:
            origin_column_input = [origin_labels.developed_acres]
        reallocate_units(mgras, candidates, selected_ID, new_acreage,
                         from_columns=origin_column_input, to_columns=[
                             product_type_labels.developed_acres])
    # infill should only subtract from itself, redev also subtracts from itself
    if origin_type.redev or origin_type.infill:
        add_to_columns_with_tracking(
            mgras, candidates, selected_ID, -1 * new_acreage,
            development_label)

    # Update square footages
    # all three origin types increase square footage
    square_feet_to_build = product_type_labels.unit_sqft_parameter() * \
        units_to_build
    add_to_columns_with_tracking(
        mgras, candidates, selected_ID, square_feet_to_build,
        product_type_labels.square_footage)
    if origin_type.redev and origin_labels is not None:
        # redevelopment should also subtract square footage from its origin
        # if it is being tracked
        safely_subtract_from_columns(
            mgras, candidates, selected_ID, square_feet_to_build,
            [origin_labels.square_footage])

    # Update unit counts
    update_units(mgras, selected_ID, units_to_build,
                 product_type_labels, candidates=candidates)
    # redeveloping should also subtract units from the original land use
    if origin_type.redev and origin_labels is not None:
        units_to_subtract = -1 * units_to_build
        update_units(mgras, selected_ID, units_to_subtract,
                     origin_labels, candidates=candidates)
        return (origin_labels, units_to_subtract)
    return None
