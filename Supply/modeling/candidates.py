import pandas
import numpy
import logging
from tqdm import tqdm

from modeling.filters import generic_filter, apply_filters
from utils.access_labels import all_product_type_labels, mgra_labels, \
    RedevelopmentLabels, ProductTypeLabels, land_origin_labels
from utils.parameter_access import parameters
from utils.pandas_shortcuts import normalize
from utils.profitability_adjust import adjust_profitability


def combine_weights(profitability, vacancy):
    '''
        Uses profitability and total units allowed by vacancy to make
        normalized weights,
        deference for vacancy, as modified by parameter scale multiplier.
    '''
    mnl_choice = parameters['use_choice_model']
    scale = parameters['scale']
    if mnl_choice:
        exponent_profitability = numpy.exp(scale*profitability)
        weights = vacancy * exponent_profitability
    else:
        # Simple weighting
        weights = vacancy + (scale * profitability)
    return normalize(weights)


def candidate_development_type(candidate, product_type_labels):
    '''
        find the land development label that corresponds to a non-NaN value.
        each candidate is created with only one non-NaN land origin value.
    '''
    possible_labels = land_origin_labels.applicable_labels_for(
        product_type_labels)
    # logging.debug('candidate check type: {}'.format(
    #     candidate[possible_labels]))
    for label in possible_labels:
        if pandas.notnull(candidate[label]).item():
            return label
    return None  # reaching this would signify a bug


def get_square_footage_per_unit(candidate, product_type_labels):
    '''
        attempts to calculate the square footage per unit on the mgra
        if either entry seems invalid, returns the average value from
        the region
    '''
    square_footage = candidate[product_type_labels.square_footage].item()
    total_units = candidate[product_type_labels.total_units].item()
    if square_footage < 1 or total_units < 1:
        return product_type_labels.unit_sqft_parameter()
    else:
        return square_footage / total_units


def get_acreage_per_unit(candidate, product_type_labels):
    '''
        same as get_square_footage_per_unit, but with developed acres
    '''
    acreage = candidate[product_type_labels.developed_acres].item()
    total_units = candidate[product_type_labels.total_units].item()
    if acreage < 1 or total_units < 1:
        return product_type_labels.land_use_per_unit_parameter()
    else:
        return acreage / total_units


class Candidates(object):
    def __init__(self, mgras):
        self.mgras = mgras.copy()
        self.mgras = adjust_profitability(self.mgras)
        self.candidates = self.create_candidate_set()
        self.candidates.reset_index(drop=True, inplace=True)
        # self.product_types = product_types()
        # self.product_type_tables = {
        #     product_type: apply_filters(
        #         self.candidates, ProductTypeLabels(product_type)
        #     ) for product_type in self.product_types
        # }

    # don't recalculate filters each time a candidate is selected... only
    # update the affected candidates each iteration?
    # we still have to re-weight every candidate, it might not make sense to
    # separate that out
    # def filter_by_product_types()

    def mgra_updated(self, mgra_id, product_type, units):
        # find and update all candidates who have had their fields changed
        # eg. reduce land available in applicable candidates with matching
        # mgra_id in every product type frame
        # another example is with units decreased.
        pass

    def select_candidate_for_product_type(self, product_type):
        # filtered = self.product_type_tables[product_type]
        filtered = apply_filters(
            self.candidates, ProductTypeLabels(product_type))
        # uncomment to debug candidate filtering
        # save_to_file(filtered, 'data/output', 'filtered_candidates.csv')
        if len(filtered) < 1:
            return None
        # Sample
        weights = combine_weights(
            filtered.profit_margin, filtered.vacancy_cap)
        # DataFrame.sample replace argument is False by default, so the
        # selected candidate will not be considered again.
        logging.debug('{} candidates left for product type {}'.format(
            len(filtered), product_type))
        selected = filtered.sample(n=1, weights=weights)
        # .sample only removed the candidate from the filtered copy, also
        # remove it from the original candidates
        self.candidates.drop([selected.index.array[0]], inplace=True)
        return selected

    def __trim_columns(self, frame, include_columns=[], remove_columns=[]):
        # drops all redev and infill columns if include_columns is not set
        # callers can specify the applicable redev columns to keep, as well
        # as other columns to remove.
        my_include_columns = mgra_labels.list_labels()
        for labels in all_product_type_labels():
            my_include_columns.extend(labels.list_labels())
        my_include_columns.extend(include_columns)
        frame = frame[my_include_columns]
        return frame.drop(remove_columns).copy()

    def create_candidate_set(self):
        # remove candidates with no vacant land (filters from 23002 to 8802)
        mgras_with_vacant_land = generic_filter(
            self.mgras, [mgra_labels.VACANT_ACRES])

        candidate_list = []
        redevelopment_labels = RedevelopmentLabels().list_labels()
        product_types = all_product_type_labels()
        progress_bar = tqdm(total=len(self.mgras) +
                            len(mgras_with_vacant_land))
        progress_bar.set_description('creating candidate set')
        # create vacant land candidates
        for _, series in mgras_with_vacant_land.iterrows():
            for label in product_types:
                if series[label.vacant_acres] != 0.0:
                    # take out all vacant land labels except our own
                    remove_columns = [
                        product.vacant_acres for product in product_types]
                    remove_columns.remove(label.vacant_acres)
                    new_candidate = self.__trim_columns(
                        series,
                        remove_columns=remove_columns)
                    candidate_list.append(new_candidate)
            progress_bar.update()
        # create Redev and infill candidates
        for _, series in self.mgras.iterrows():
            for label in redevelopment_labels:
                if series[label] != 0.0:
                    # now the row will have nan's for the normal vacant acres
                    # and the other redevelopment labels when merged with the
                    # other candidates
                    new_candidate = self.__trim_columns(
                        series,
                        include_columns=[label],
                        remove_columns=[
                            product.vacant_acres for product in
                            all_product_type_labels()
                        ]
                    )
                    candidate_list.append(new_candidate)
            progress_bar.update()
        progress_bar.close()
        # save_to_file(candidates, 'data/output', 'candidates.csv')
        return pandas.DataFrame(candidate_list).copy()

    def remove_redev_from(self, product_type):
        # remove any candidates whose selection would reduce the built supply
        # of the product type corresponding to label
        applicable_labels = RedevelopmentLabels().all_labels_for_origin(
            product_type
        )
        logging.debug(
            "removing candidates that would use product type {}".format(
                product_type.product_type
            )
        )
        self.candidates.loc[:, applicable_labels] = None
