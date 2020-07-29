import unittest
import os
import pandas
import logging

from utils.constants import INCREASING_COLUMNS, DECREASING_COLUMNS

COMMANDLINE_INPUT = 'python3 meet_demand.py -t'


class TestMeetDemand(unittest.TestCase):

    def setUp(self):
        self.expected_file_1 = 'test_data/random_MGRA.csv'
        self.expected_file_2 = 'test_data/output/year1_2013.csv'
        return

    def test_meet_demand(self):
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
        for column in INCREASING_COLUMNS:
            logging.info(column)
            self.assertGreater(
                frame_after[column].sum(),
                frame_before[column].sum())

        logging.info('ensuring that columns decreased')

        for column in DECREASING_COLUMNS:
            logging.info(column)
            self.assertLess(frame_after[column].sum(),
                            frame_before[column].sum())