
import pandas
from utils.constants import REDM_IO_COLUMNS

'''
    Accepts the v4 input file and the interpolated variables from manhan group
    creates a new input file with just the REDM applicable columns 
'''


def create_version_4point1():
    original_dataframe = pandas.read_csv("data/SRF_Input_Base_V4.csv")
    return original_dataframe


if __name__ == "__main__":
    create_version_4point1()
