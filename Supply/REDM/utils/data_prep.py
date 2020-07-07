
import pandas
from utils.constants import REDM_IO_COLUMNS, MGRA, PRODUCT_TYPES
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


def add_job_units_columns(dataframe):
    for product_type in PRODUCT_TYPES:
        pass
    pass


def create_version_4point1():
    original_frame = pandas.read_csv("data/SRF_Input_Base_V4.csv")
    interpolated_frame = load_interpolated()
    combined_frame = pandas.merge(original_frame, interpolated_frame, on=MGRA)
    final_frame = combined_frame[REDM_IO_COLUMNS]
    save_to_file(final_frame, 'data', 'SRF_Input_Base_V4.1.csv')
    return


if __name__ == "__main__":
    create_version_4point1()
