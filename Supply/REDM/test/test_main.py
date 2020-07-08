import unittest
import os
import pandas
import logging

from utils.constants import DEVELOPED_ACRES, SINGLE_FAMILY_DEVELOPED_ACRES, \
    SINGLE_FAMILY_HOUSING_UNITS, SINGLE_FAMILY_TOTAL_SQUARE_FOOTAGE, \
    MULTI_FAMILY_DEVELOPED_ACRES, MULTI_FAMILY_HOUSING_UNITS, \
    MULTI_FAMILY_TOTAL_SQUARE_FOOTAGE, OFFICE_DEVELOPED_ACRES, \
    OFFICE_BUILDINGS, OFFICE_TOTAL_SQUARE_FOOTAGE, \
    INDUSTRIAL_DEVELOPED_ACRES, INDUSTRIAL_BUILDINGS, \
    INDUSTRIAL_TOTAL_SQUARE_FOOTAGE, COMMERCIAL_DEVELOPED_ACRES, \
    COMMERCIAL_BUILDINGS, COMMERCIAL_TOTAL_SQUARE_FOOTAGE, \
    SINGLE_FAMILY_VACANT_ACRES, MULTI_FAMILY_VACANT_ACRES, \
    OFFICE_VACANT_ACRES, INDUSTRIAL_VACANT_ACRES, COMMERCIAL_VACANT_ACRES, \
    VACANT_ACRES, HOUSING_UNITS, OFFICE_JOB_SPACES, COMMERCIAL_JOB_SPACES, \
    INDUSTRIAL_JOB_SPACES

COMMANDLINE_INPUT = 'python redm_main.py -t'


class TestMain(unittest.TestCase):

    def setUp(self):
        self.expected_file_1 = 'test_data/output/year1_2013.csv'
        self.expected_file_2 = 'test_data/output/year2_2014.csv'
        return

    def test_redm_main(self):
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
                              MULTI_FAMILY_TOTAL_SQUARE_FOOTAGE,
                              OFFICE_DEVELOPED_ACRES, OFFICE_BUILDINGS,
                              OFFICE_TOTAL_SQUARE_FOOTAGE,
                              INDUSTRIAL_DEVELOPED_ACRES, INDUSTRIAL_BUILDINGS,
                              INDUSTRIAL_TOTAL_SQUARE_FOOTAGE,
                              COMMERCIAL_DEVELOPED_ACRES, COMMERCIAL_BUILDINGS,
                              COMMERCIAL_TOTAL_SQUARE_FOOTAGE, HOUSING_UNITS,
                              OFFICE_JOB_SPACES, COMMERCIAL_JOB_SPACES,
                              INDUSTRIAL_JOB_SPACES]
        for column in increasing_columns:
            logging.info(column)
            self.assertGreater(
                frame_after[column].sum(),
                frame_before[column].sum())

        logging.info('ensuring that columns decreased')
        decreasing_columns = [VACANT_ACRES, SINGLE_FAMILY_VACANT_ACRES,
                              MULTI_FAMILY_VACANT_ACRES, OFFICE_VACANT_ACRES,
                              INDUSTRIAL_VACANT_ACRES, COMMERCIAL_VACANT_ACRES]
        for column in decreasing_columns:
            logging.info(column)
            self.assertLess(frame_after[column].sum(),
                            frame_before[column].sum())
