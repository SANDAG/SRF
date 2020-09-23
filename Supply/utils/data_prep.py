import pandas

from utils.interface import save_to_file
from utils.access_labels import mgra_labels, residential_types, \
    non_residential_types, ProductTypeLabels, all_columns
'''
    Accepts the v4 input file and the interpolated variables from manhan group
    creates a new input file with just the Supply applicable columns
'''


def sort_by_column(frame, column):
    # puts frame in column ascending order. re-indexes
    return frame.sort_values(column).reset_index()


def load_interpolated():
    return sort_by_column(
        pandas.read_csv('data/interpolation_results.csv'), mgra_labels.MGRA
    )


def job_spaces_for_product_type(dataframe, product_type):
    # get applicable columns
    labels = ProductTypeLabels(product_type)
    average_area_per_job = dataframe[labels.job_area]
    current_employment = dataframe[labels.occupied_units]
    total_area = dataframe[labels.square_footage]
    # find estimate of unoccupied job spaces
    used_area = average_area_per_job * current_employment
    vacant_area = total_area - used_area
    unoccupied_job_spaces = vacant_area / average_area_per_job
    # if negative, assume that the spaces are all occupied
    unoccupied_job_spaces[unoccupied_job_spaces < 0] = 0
    total_job_spaces = current_employment + \
        unoccupied_job_spaces.astype('int32')
    return total_job_spaces


def add_job_spaces_columns(dataframe):
    # start column for total job spaces
    dataframe[mgra_labels.TOTAL_JOB_SPACES] = 0
    # create job spaces column for each non-residential type
    for product_type in non_residential_types:
        labels = ProductTypeLabels(product_type)
        dataframe[labels.total_units] = job_spaces_for_product_type(
            dataframe, product_type)
        # also add to the total job spaces column
        dataframe[mgra_labels.TOTAL_JOB_SPACES] += dataframe[
            labels.total_units]
    return dataframe


def fix_capacity(dataframe):
    '''
        capacity values are unfortunately the leftover capacity, not the total
        capacity.
        Add together the current units and the leftover capacity to find the
        total, then replace the previous values
    '''
    dataframe[mgra_labels.HOUSING_CAPACITY] += dataframe[
        mgra_labels.HOUSING_UNITS]
    for product_type in residential_types:
        labels = ProductTypeLabels(product_type)
        dataframe[labels.capacity] += dataframe[labels.total_units]
    return dataframe


def create_version_4point1():
    original_frame = pandas.read_csv("data/SRF_Input_Base_V4.csv")
    # add interpolated variables
    interpolated_frame = load_interpolated().drop([mgra_labels.LUZ], axis=1)
    combined_frame = pandas.merge(
        original_frame, interpolated_frame, on=mgra_labels.MGRA)
    # add job spaces
    frame_with_job_spaces = add_job_spaces_columns(combined_frame)
    # fix capacity
    frame_with_fixed_capacity = fix_capacity(frame_with_job_spaces)
    # remove unused columns
    final_frame = frame_with_fixed_capacity[all_columns()]
    save_to_file(final_frame, 'data', 'SRF_Input_Base_V4.1.csv')
    return


if __name__ == "__main__":
    create_version_4point1()
