import unittest
import os
import pandas
import logging

from utils.access_labels import increasing_columns, decreasing_columns
from utils.interface import parameters

COMMANDLINE_INPUT = 'python meet_demand.py -t'


class TestMeetDemand(unittest.TestCase):

    def setUp(self):
        self.expected_file_1 = 'data/SRF_Input_Base_V4.1.csv'
        self.expected_file_2 = 'test_data/output/forecasted_year_2013.csv'
        return

    def test_meet_demand(self):
        # skip this integration test if there is an argument given to
        # the test runner
        if not parameters['include_integration_tests']:
            return unittest.skip('commandline argument given')

        result = os.system(COMMANDLINE_INPUT)
        self.assertEqual(result, 0)

        # check that all columns were updated as expected
        try:
            frame_before = pandas.read_csv(self.expected_file_1)
            frame_after = pandas.read_csv(self.expected_file_2)
        except FileNotFoundError:
            self.fail("could not read files, \'{}\' likely failed".format(
                COMMANDLINE_INPUT))

        logging.info('ensuring that columns increased:')
        for column in increasing_columns():
            logging.info("column: {} (sum: {})".format(
                column, frame_before[column].sum()))
            self.assertGreater(
                frame_after[column].sum(),
                frame_before[column].sum(),
                '{} did not increase, not a breaking error'.format(column))

        logging.info('ensuring that columns decreased:')

        for column in decreasing_columns():
            logging.info(column)
            self.assertLess(
                frame_after[column].sum(),
                frame_before[column].sum(),
                '{} did not decrease, not a breaking error'.format(column))

    # ensure that tests can trigger a setting with copy warning
    # def test_pandas_setting_with_copy_warning(self):
    #     data = pandas.DataFrame({
    #         "foo": [1, 2, 3, 4],
    #         "bar": [5, 6, 7, 8]
    #     })

    #     data[data.foo == 1]['bar'] = 100
