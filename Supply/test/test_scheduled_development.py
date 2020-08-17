import unittest
import os
import pandas
import logging
import sys

from utils.access_labels import increasing_columns, decreasing_columns

COMMANDLINE_INPUT = 'python3 scheduled_development.py -t'


class TestMain(unittest.TestCase):

    def setUp(self):
        self.expected_file_1 = 'data/SRF_Input_Base_V4.1.csv'
        self.expected_file_2 = 'data/output/planned_development_added.csv'
        return

    def test_main(self):
        if len(sys.argv) > 1:
            return
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

        for column in increasing_columns():
            logging.info(column)
            self.assertGreater(
                frame_after[column].sum(),
                frame_before[column].sum())

        logging.info('ensuring that columns decreased')

        for column in decreasing_columns():
            logging.info(column)
            self.assertLess(frame_after[column].sum(),
                            frame_before[column].sum())
