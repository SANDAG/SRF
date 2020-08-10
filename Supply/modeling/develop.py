import logging
import numpy
from tqdm import tqdm

from modeling.filters import apply_filters
from modeling.dataframe_updates import update_mgra
from utils.access_labels import product_types, ProductTypeLabels, mgra_labels


def buildable_units(mgra, product_type_labels, max_units, vacancy_caps):
    acreage_per_unit = product_type_labels.land_use_per_unit_parameter()
    # determine max units to build
    vacancy_cap = vacancy_caps.loc[mgra.index].values.item()

    # TODO: also use profitability filter value for this mgra
    # to determine the number of profitable units to build.

    # only build up to 95% of the vacant space
    available_units_by_land = mgra[
        product_type_labels.vacant_acres].values.item() * \
        0.95 // acreage_per_unit

    logging.debug('max: {}, vacancy: {}, by land {}'.format(
        max_units, vacancy_cap, available_units_by_land))
    return int(min(max_units,
                   vacancy_cap, available_units_by_land))


def normalize(collection):
    # works with pandas Series and numpy arrays
    return collection / collection.sum()


def combine_weights(profitability, vacancy, preference=1):
    '''
        Prioritizes profitability to make selections, with some
        deference for vacancy, as modified by preference multiplier.
    '''
    weights = vacancy * preference * numpy.exp(profitability)
    return normalize(weights)


def develop_product_type(mgras, product_type_labels):
    new_units_to_build = product_type_labels.units_per_year_parameter()
    built_units = 0
    progress_bar = tqdm(total=new_units_to_build)
    progress_bar.set_description(
        "developing {} units".format(product_type_labels.product_type))
    while built_units < new_units_to_build:
        max_units = new_units_to_build - built_units

        # Filter
        filtered, vacancy_caps, profit_margins = apply_filters(
            mgras, product_type_labels)

        if len(filtered) < 1:
            print('out of usable mgras for product type {}'.format(
                product_type_labels.product_type))
            print('evaluate filtering methods\nexiting')
            return None

        # Sample
        # vacancy_weights = normalize(vacancy_caps)
        # profit_weights = normalize(profits)
        weights = combine_weights(profit_margins, vacancy_caps)
        selected_row = filtered.sample(n=1, weights=weights)
        selected_ID = selected_row[mgra_labels.MGRA].iloc[0]

        buildable_count = buildable_units(
            selected_row, product_type_labels, max_units, vacancy_caps)
        built_units += buildable_count
        logging.debug('building {} {} units on MGRA #{}'.format(
            buildable_count, product_type_labels.product_type, selected_ID))

        # develop buildable_count units by updating the MGRA in the dataframe
        update_mgra(mgras, selected_ID,
                    buildable_count, product_type_labels)
        progress_bar.update(buildable_count)

    progress_bar.close()

    return mgras


def develop(mgras):
    """
    Arguments
        mgras:
            A pandas dataframe of mgra's that will be updated with new values
            based on demand inputs found in parameters.yaml
    Returns:
        a pandas dataframe with selected MGRA's updated
    """
    for product_type in product_types():
        product_type_labels = ProductTypeLabels(product_type)
        mgras = develop_product_type(
            mgras, product_type_labels)
        if mgras is None:
            return mgras

    return mgras
