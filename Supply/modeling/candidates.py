import pandas
from tqdm import tqdm

from modeling.filters import generic_filter
from utils.access_labels import all_product_type_labels, mgra_labels, \
    RedevelopmentLabels


def trim_columns(frame, include_columns=[], remove_columns=[]):
    # drops all redev and infill columns if include_columns is not set
    # callers can specify the applicable redev columns to keep, as well
    # as other columns to remove.
    my_include_columns = mgra_labels.list_labels()
    for labels in all_product_type_labels():
        my_include_columns.extend(labels.list_labels())
    my_include_columns.extend(include_columns)
    frame = frame[my_include_columns]
    return frame.drop(remove_columns).copy()


def create_candidate_set(mgras):
    candidates = mgras.copy()
    mgras_with_vacant_land = mgras.copy()
    # remove candidates with no vacant land (filters from 23002 to 8802)
    candidates = generic_filter(candidates, [mgra_labels.VACANT_ACRES]).copy()

    candidate_list = []
    redevelopment_labels = RedevelopmentLabels().list_labels()
    product_types = all_product_type_labels()
    progress_bar = tqdm(total=len(mgras) + len(mgras_with_vacant_land))
    progress_bar.set_description('creating candidate set')

    for index, series in mgras_with_vacant_land.iterrows():
        # create vacant land candidates
        for label in product_types:
            if series[label.vacant_acres] != 0.0:
                other_product_types = all_product_type_labels()
                remove_columns = [
                    product.vacant_acres for product in other_product_types]
                remove_columns.remove(label.vacant_acres)
                new_candidate = trim_columns(
                    series,
                    remove_columns=remove_columns)
                candidate_list.append(new_candidate)
        progress_bar.update()

    for index, series in mgras.iterrows():
        # create Redev and infill candidates
        for label in redevelopment_labels:
            if series[label] != 0.0:
                # now the row will have nan's for the normal vacant acres and
                # the other redevelopment labels when merged with the other
                # candidates
                new_candidate = trim_columns(
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
