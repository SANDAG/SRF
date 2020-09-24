import unittest
import pandas

from modeling.dataframe_updates import add_to_columns, reallocate_units, \
    update_mgra, increment_building_ages
from utils.interface import parameters
import utils.access_labels as access
from utils.access_labels import ProductTypeLabels


class TestDataframeUpdates(unittest.TestCase):
    def setUp(self):
        self.test_mgras = pandas.read_csv(parameters['input_filename'])
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
        random_mgra = self.test_mgras.sample(random_state=19)
        self.assertIsNone(
            update_mgra(
                self.test_mgras,
                random_mgra, 10, self.product_type_labels,
                scheduled_development=False)
        )

    def test_increment_building_ages(self):
        mgra_label = "MGRA"
        single_family_labels = self.product_type_labels
        multi_family_labels = ProductTypeLabels('multi_family')
        '''
            mgra 1: 12 units, 4 new, 3 old, 5 normal
            mgra 2: 100 units, 2 new, 4 old, 94 normal
            mgra 3: 56 units, 5 new, 10 old, 41 normal
            mgra 4: 350 units, 35 new, 175 old, 140 normal
        '''
        housing_age_frame = pandas.DataFrame({
            mgra_label: [1, 2],
            single_family_labels.proportion_new: [0.33, 0.02],
            single_family_labels.proportion_old: [0.25, 0.04],
            single_family_labels.total_units: [12, 100],
            multi_family_labels.proportion_new: [0.0892, 0.1],
            multi_family_labels.proportion_old: [0.1785, 0.5],
            multi_family_labels.total_units: [56, 350]
        })
        increment_building_ages(housing_age_frame)
        self.assertAlmostEqual(
            0.297,
            housing_age_frame.loc[
                housing_age_frame[mgra_label] ==
                1, single_family_labels.proportion_new].item()
        )
        self.assertAlmostEqual(
            0.26041666,
            housing_age_frame.loc[
                housing_age_frame[mgra_label] ==
                1, single_family_labels.proportion_old].item(), 2
        )
        self.assertAlmostEqual(
            0.0, housing_age_frame.loc[
                housing_age_frame[mgra_label] == 2,
                multi_family_labels.proportion_new].item()
        )

    def test_correct_building_ages(self):
        pass
