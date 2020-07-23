import unittest
import os
import pandas
import logging

from utils.constants import DEVELOPED_ACRES, SINGLE_FAMILY_DEVELOPED_ACRES, \
    SINGLE_FAMILY_HOUSING_UNITS, SINGLE_FAMILY_TOTAL_SQUARE_FOOTAGE, \
    MULTI_FAMILY_DEVELOPED_ACRES, MULTI_FAMILY_HOUSING_UNITS, \
    MULTI_FAMILY_TOTAL_SQUARE_FOOTAGE, \
    SINGLE_FAMILY_VACANT_ACRES, MULTI_FAMILY_VACANT_ACRES, \
    VACANT_ACRES, HOUSING_UNITS, OFFICE_DEVELOPED_ACRES, OFFICE_JOB_SPACES, \
    OFFICE_TOTAL_SQUARE_FOOTAGE, COMMERCIAL_DEVELOPED_ACRES, \
    COMMERCIAL_JOB_SPACES, COMMERCIAL_TOTAL_SQUARE_FOOTAGE, \
    INDUSTRIAL_DEVELOPED_ACRES, INDUSTRIAL_JOB_SPACES, \
    INDUSTRIAL_TOTAL_SQUARE_FOOTAGE

COMMANDLINE_INPUT = 'python3 scheduled_development.py'


class TestMain(unittest.TestCase):

    def setUp(self):
        self.expected_file_1 = 'data/SRF_Input_Base_V4.1.csv'
        self.expected_file_2 = 'data/output/planned_development_added.csv'
        return

    def test_main(self):
        result = os.system(COMMANDLINE_INPUT)
        self.assertEqual(result, 0)

        # check that all columns were updated as expected
        try:
            frame_before = pandas.read_csv(self.expected_file_1)
            frame_after = pandas.read_csv(self.expected_file_2)
        except FileNotFoundError:
            self.fail("could not read files, \'{}\' likely failed".format(
                COMMANDLINE_INPUT))

        logging.info('ensuring that columns increased')
        increasing_columns = [DEVELOPED_ACRES, SINGLE_FAMILY_DEVELOPED_ACRES,
                              SINGLE_FAMILY_HOUSING_UNITS,
                              SINGLE_FAMILY_TOTAL_SQUARE_FOOTAGE,
                              MULTI_FAMILY_DEVELOPED_ACRES,
                              MULTI_FAMILY_HOUSING_UNITS,
                              MULTI_FAMILY_TOTAL_SQUARE_FOOTAGE, HOUSING_UNITS,
                              OFFICE_DEVELOPED_ACRES, OFFICE_JOB_SPACES,
                              OFFICE_TOTAL_SQUARE_FOOTAGE,
                              COMMERCIAL_DEVELOPED_ACRES,
                              COMMERCIAL_JOB_SPACES,
                              COMMERCIAL_TOTAL_SQUARE_FOOTAGE,
                              INDUSTRIAL_DEVELOPED_ACRES,
                              INDUSTRIAL_JOB_SPACES,
                              INDUSTRIAL_TOTAL_SQUARE_FOOTAGE]
        for column in increasing_columns:
            logging.info(column)
            self.assertGreater(
                frame_after[column].sum(),
                frame_before[column].sum())

        logging.info('ensuring that columns decreased')
        decreasing_columns = [VACANT_ACRES, SINGLE_FAMILY_VACANT_ACRES,
                              MULTI_FAMILY_VACANT_ACRES]
        for column in decreasing_columns:
            logging.info(column)
            self.assertLess(frame_after[column].sum(),
                            frame_before[column].sum())
