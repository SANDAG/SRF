import logging

from modeling.filters import apply_filters
from modeling.dataframe_updates import update_mgra
from utils.constants import MGRA, ProductTypeLabels, PRODUCT_TYPES


def buildable_units(mgra, product_type_labels, max_units, vacancy_caps):
    acreage_per_unit = product_type_labels.land_use_per_unit_parameter()
    # determine max units to build
    vacancy_cap = vacancy_caps.loc[mgra.index].values.item()

    # TODO: also use profitability filter value for this mgra
    # to determine the number of profitable units to build.

    # TODO: use capacity values for residential
    if product_type_labels.is_residential():
        pass

    # only build up to 95% of the vacant space
    available_units_by_land = mgra[
        product_type_labels.vacant_acres].values.item() * \
        0.95 // acreage_per_unit

    logging.debug('max: {}, vacancy: {}, by land {}'.format(
        max_units, vacancy_cap, available_units_by_land))
    return int(min(max_units,
                   vacancy_cap, available_units_by_land))


def normalize(dataframe):
    # also works with pandas Series
    return (dataframe - dataframe.min()) / (dataframe.max() - dataframe.min())


def develop_product_type(mgras, product_type_labels, progress):
    if progress is not None:
        progress.set_description('developing {}'.format(
            product_type_labels.product_type))

    new_units_to_build = product_type_labels.units_per_year_parameter()
    logging.debug('building {} units'.format(new_units_to_build))
    built_units = 0
    while built_units < new_units_to_build:
        max_units = new_units_to_build - built_units

        # Filter
        filtered, vacancy_caps, profits = apply_filters(
            mgras, product_type_labels)

        if len(filtered) < 1:
            print('out of usable mgras for product type {}'.format(
                product_type_labels.product_type))
            print('evaluate filtering methods\nexiting')
            return None, progress

        # Sample
        # vacancy_weights = normalize(vacancy_caps)
        # profit_weights = normalize(profits)
        selected_row = filtered.sample(n=1, weights=vacancy_caps)
        selected_ID = selected_row[MGRA].iloc[0]

        buildable_count = buildable_units(
            selected_row, product_type_labels, max_units, vacancy_caps)
        built_units += buildable_count

        logging.debug('building {} {} units on MGRA #{}'.format(
            buildable_count, product_type_labels.product_type, selected_ID))

        # develop buildable_count units by updating the MGRA in the dataframe
        update_mgra(mgras, selected_ID,
                    buildable_count, product_type_labels)

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
    for product_type in PRODUCT_TYPES:
        product_type_labels = ProductTypeLabels(product_type)
        mgras, progress = develop_product_type(
            mgras, product_type_labels, progress)
        if mgras is None:
            return mgras, progress

    # tests don't use a progress bar
    if progress is not None:
        return mgras, progress
    else:
        return mgras
