import unittest

import pandas

from modeling.dataframe_updates import add_to_columns
from utils.interface import parameters
import utils.access_labels as access
from utils.access_labels import ProductTypeLabels


class TestDataframeUpdates(unittest.TestCase):
    def setUp(self):
        self.test_frame = pandas.read_csv(parameters['input_filename'])

    def test_add_to_columns(self):
        housing_label = access.mgra_labels.HOUSING_UNITS
        specific_label = ProductTypeLabels().total_units
        total_housing_before = self.test_frame[housing_label].sum()
        single_family_units_before = \
            self.test_frame[specific_label].sum()

        mgra_id = self.test_frame.sample()[access.mgra_labels.MGRA].iloc[0]
        units = 1
        add_to_columns(
            self.test_frame, mgra_id, units,
            [housing_label, specific_label]
        )

        self.assertGreater(
            self.test_frame[housing_label].sum(), total_housing_before
        )
        self.assertGreater(
            self.test_frame[specific_label].sum(),
            single_family_units_before
        )
