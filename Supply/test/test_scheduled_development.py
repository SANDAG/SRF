import unittest
import os
import pandas
import logging

from utils.access_labels import increasing_columns, decreasing_columns, \
    ProductTypeLabels
from utils.interface import parameters

from scheduled_development import pick_labels_with_highest_value, \
    total_for_luz, find_largest_luz_employment_type, \
    find_current_employment_type

COMMANDLINE_INPUT = 'python scheduled_development.py -t'


class TestMain(unittest.TestCase):

    def setUp(self):
        self.expected_file_1 = 'data/SRF_Input_Base_V4.1.csv'
        self.expected_file_2 = 'data/output/scheduled_development_added.csv'

        self.industrial_labels = ProductTypeLabels("industrial")
        self.commercial_labels = ProductTypeLabels("commercial")
        self.office_labels = ProductTypeLabels("office")

        return

    def test_main(self):
        # skip this integration test if there is an argument given to
        # the test runner
        if parameters['omit_integration_tests']:
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

    def test_pick_labels_with_highest_value(self):
        a_labels = ["1", "2", "3"]
        a_values = [1, 2, 3]
        self.assertEqual(
            "3", pick_labels_with_highest_value(a_labels, a_values))

        # the first instance of the max
        duplicate_max_labels = [1, 2, 3, 4, 5]
        duplicate_max_values = [1, 2, 3, 4, 4]
        self.assertAlmostEqual(4, pick_labels_with_highest_value(
            duplicate_max_labels, duplicate_max_values))

    def test_total_for_luz(self):
        mgra_frame = pandas.DataFrame({
            "LUZ": [1, 1, 1, 1, 1, 3],
            "units": [10, 1, 0, 4, 5, 100]
        })
        self.assertEqual(20, total_for_luz(
            mgra_frame, mgra_frame.iloc[0, 0], "units"))

    def test_find_largest_luz_employment_type(self):
        mgra_frame = pandas.DataFrame({
            "LUZ": [1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
            self.industrial_labels.total_units: [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            self.commercial_labels.total_units: [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            self.office_labels.total_units:     [1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
        })
        self.assertEqual(
            self.office_labels.product_type,
            find_largest_luz_employment_type(mgra_frame, 1).product_type
        )
        self.assertEqual(
            self.industrial_labels.product_type,
            find_largest_luz_employment_type(mgra_frame, 2).product_type
        )

    def test_find_current_employment_type(self):
        mgra_frame = pandas.DataFrame({
            "MGRA": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "LUZ": [1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
            self.industrial_labels.total_units: [0, 0, 1, 1, 0, 0, 2, 2, 1, 0],
            self.commercial_labels.total_units: [0, 1, 0, 1, 1, 1, 1, 2, 3, 0],
            self.office_labels.total_units:     [1, 0, 0, 0, 1, 3, 0, 3, 2, 0]
        })

        office = self.office_labels.product_type
        commercial = self.commercial_labels.product_type
        industrial = self.industrial_labels.product_type

        correct_answers = [
            office, commercial, industrial, industrial, commercial,
            office, industrial, office, commercial, office
        ]

        for i in range(len(mgra_frame)):
            self.assertEqual(
                correct_answers[i],
                find_current_employment_type(
                    mgra_frame, mgra_frame.iloc[i]).product_type,
                "index: {}".format(i)
            )
