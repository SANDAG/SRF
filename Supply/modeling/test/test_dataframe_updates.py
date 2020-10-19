import unittest
import pandas

from modeling.dataframe_updates import add_to_columns, reallocate_units, \
    update_mgra
from utils.interface import parameters
import utils.access_labels as access
from utils.access_labels import ProductTypeLabels


class TestDataframeUpdates(unittest.TestCase):
    def setUp(self):
        # self.test_mgras = pandas.read_csv(parameters['input_filename'])
        self.test_mgras = pandas.read_csv('test_data/random_MGRA.csv')

        self.product_type_labels = ProductTypeLabels('single_family')

    def test_add_to_columns(self):
        housing_label = access.mgra_labels.HOUSING_UNITS
        specific_label = ProductTypeLabels().total_units
        total_housing_before = self.test_mgras[housing_label].sum()
        single_family_units_before = \
            self.test_mgras[specific_label].sum()

        mgra_id = self.test_mgras.sample()[access.mgra_labels.MGRA].iloc[0]
        units = 1
        add_to_columns(
            self.test_mgras, mgra_id, units,
            [housing_label, specific_label]
        )

        self.assertGreater(
            self.test_mgras[housing_label].sum(), total_housing_before
        )
        self.assertGreater(
            self.test_mgras[specific_label].sum(),
            single_family_units_before
        )

    def test_reallocate_units(self):
        mgras = pandas.DataFrame({
            "MGRA": [1, 2, 3, 4, 5],
            "departures": [12, 35, 21, 45, 0],
            "arrivals": [9, 4, 24, 59, 0],
        })
        # begin_departure = 12
        # begin_arrival = 9
        transfer_count = 3
        reallocate_units(mgras, 1, transfer_count, [
                         'departures'], ['arrivals'])
        self.assertEqual(9, mgras['departures'].values[0])
        self.assertEqual(12, mgras['arrivals'].values[0])

    def test_update_mgra(self):
        # print(self.test_mgras.iloc[1223, :])
        random_mgra = self.test_mgras.sample(random_state=19)
        self.assertIsNone(
            update_mgra(
                self.test_mgras,
                random_mgra, 10, self.product_type_labels,
                scheduled_development=False)
        )
