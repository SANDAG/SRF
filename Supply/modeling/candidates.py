import pandas
from tqdm import tqdm

from utils.access_labels import all_product_type_labels, mgra_labels, \
    RedevelopmentLabels

# if we have one set of candidates.... can the set determine if one candidate
# doesn't work for any product type and take it out of consideration?


# options for inserting redevelopment considerations as candidates...
# replace the usual fields for consideration with the redev applicable ones,
# remembering that an operation will need to happen on the other side

# add a column specifying exactly what type of construction should happen, and
#  modify the labels used based on that.

# make the other options NaN, only the applicable developable acreage column
# for this candidate is not NaN. - Going with this option for now


# still have "candidates", just as a specialized dataframe

def trim_columns(frame, include_columns=[], remove_columns=[]):
    # drops all redev and infill columns if include_columns is not set
    # callers can specify the applicable redev columns to keep.
    for labels in all_product_type_labels():
        include_columns.extend(labels.list_labels())
    include_columns.extend(mgra_labels.list_labels())

    frame = frame[include_columns]
    return frame.drop(remove_columns)


def make_redev_candidates(mgra_dataframe):
    # since redevelopment has a bunch of labels that are hard to iterate
    # through, just do it by hand
    redev_labels = RedevelopmentLabels()
    candidate_list = []
    progress_bar = tqdm(total=len(mgra_dataframe))
    progress_bar.set_description('creating redev and infill candidate set')
    for index, series in mgra_dataframe.iterrows():
        for label in redev_labels.list_labels():
            if series[label] != 0.0:
                # now the row will have nan's for the normal vacant acres and
                # the other redevelopment labels when merged with the other
                # candidates
                candidate_list.append(
                    trim_columns(
                        series, include_columns=[label],
                        remove_columns=[
                            product.vacant_acres for product in
                            all_product_type_labels()
                        ]
                    )
                )
                # candidate_list.append(series)
        progress_bar.update()
    progress_bar.close()

    return pandas.DataFrame(candidate_list)
