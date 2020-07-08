
import pandas
from utils.constants import REDM_IO_COLUMNS, MGRA, NON_RESIDENTIAL_TYPES, \
    ProductTypeLabels, OFFICE_JOB_SPACES, COMMERCIAL_JOB_SPACES, INDUSTRIAL_JOB_SPACES
from utils.interface import save_to_file

'''
    Accepts the v4 input file and the interpolated variables from manhan group
    creates a new input file with just the REDM applicable columns
'''


def sort_by_column(frame, column):
    # puts frame in column ascending order. re-indexes
    return frame.sort_values(column).reset_index()


def load_interpolated():
    return sort_by_column(pandas.read_csv('data/interpolated_vars.csv'), MGRA)


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
    for product_type in NON_RESIDENTIAL_TYPES:
        dataframe[product_type +
                  '_js'] = job_spaces_for_product_type(dataframe, product_type)
    dataframe['job_spaces'] = dataframe[OFFICE_JOB_SPACES] + \
        dataframe[COMMERCIAL_JOB_SPACES] + dataframe[INDUSTRIAL_JOB_SPACES]
    return dataframe


def create_version_4point1():
    original_frame = pandas.read_csv("data/SRF_Input_Base_V4.csv")
    interpolated_frame = load_interpolated()
    combined_frame = pandas.merge(original_frame, interpolated_frame, on=MGRA)
    frame_with_job_spaces = add_job_spaces_columns(combined_frame)
    final_frame = frame_with_job_spaces[REDM_IO_COLUMNS]
    save_to_file(final_frame, 'data', 'SRF_Input_Base_V4.1.csv')
    return


if __name__ == "__main__":
    create_version_4point1()
