import unittest
import pandas

from modeling.dataframe_updates import add_to_columns, reallocate_units, \
    update_mgra, increment_building_ages, update_units
from utils.interface import parameters
import utils.access_labels as access
from utils.access_labels import ProductTypeLabels
from utils.pandas_shortcuts import get_item


class TestDataframeUpdates(unittest.TestCase):
    def setUp(self):
        self.test_mgras = pandas.read_csv(parameters['input_filename'])
        self.product_type_labels = ProductTypeLabels('single_family')

        self.mgra_label = "MGRA"
        self.single_family_labels = self.product_type_labels
        self.multi_family_labels = ProductTypeLabels('multi_family')
        '''
            mgra 1: 12 units, 4 new, 3 old, 5 normal
            mgra 2: 100 units, 2 new, 4 old, 94 normal
            mgra 3: 56 units, 5 new, 10 old, 41 normal
            mgra 4: 350 units, 35 new, 175 old, 140 normal
        '''
        self.housing_age_frame = pandas.DataFrame({
            self.mgra_label: [1, 2],
            self.single_family_labels.proportion_new: [0.333333, 0.02],
            self.single_family_labels.proportion_old: [0.25, 0.04],
            self.single_family_labels.total_units: [12, 100],
            self.multi_family_labels.proportion_new: [0.0892, 0.1],
            self.multi_family_labels.proportion_old: [0.1785, 0.5],
            self.multi_family_labels.total_units: [56, 350],
            access.mgra_labels.HOUSING_UNITS: [68, 450]
        })

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
        increment_building_ages(self.housing_age_frame)
        self.assertAlmostEqual(
            0.2999997,
            get_item(self.housing_age_frame, self.mgra_label,
                     1, self.single_family_labels.proportion_new)
        )
        self.assertAlmostEqual(
            0.26041666,
            get_item(self.housing_age_frame, self.mgra_label,
                     1, self.single_family_labels.proportion_old),
            places=2
        )
        self.assertAlmostEqual(
            0.09, get_item(self.housing_age_frame, self.mgra_label,
                           2, self.multi_family_labels.proportion_new)
        )

    def test_correct_building_ages(self):
        # Test adding units
        update_units(self.housing_age_frame, 1, 10, self.single_family_labels)
        self.assertEqual(
            22,
            get_item(
                self.housing_age_frame, self.mgra_label,
                1, self.single_family_labels.total_units)
        )
        UPDATED_NEW_UNITS_COUNT = 14
        TOTAL_UNITS_AFTER_UPDATING = 22
        self.assertAlmostEqual(
            UPDATED_NEW_UNITS_COUNT / TOTAL_UNITS_AFTER_UPDATING,
            get_item(
                self.housing_age_frame,
                self.mgra_label, 1, self.single_family_labels.proportion_new),
            places=6)

        PREVIOUS_OLD_UNITS_COUNT = 3
        self.assertAlmostEqual(
            PREVIOUS_OLD_UNITS_COUNT / TOTAL_UNITS_AFTER_UPDATING,
            get_item(self.housing_age_frame, self.mgra_label, 1,
                     self.single_family_labels.proportion_old)
        )

        # Test removing units
        update_units(self.housing_age_frame, 2, -2, self.single_family_labels)
        self.assertEqual(
            98, get_item(self.housing_age_frame,
                         self.mgra_label, 2,
                         self.single_family_labels.total_units)
        )
        updated_old_units = 2
        total_units_after_removal = 98
        self.assertAlmostEqual(
            updated_old_units / total_units_after_removal,
            get_item(self.housing_age_frame, self.mgra_label, 2,
                     self.single_family_labels.proportion_old)
        )

        # test removing enough units to remove all old units and start
        # removing middle aged units
        update_units(self.housing_age_frame, 2, -2, self.single_family_labels)
        self.assertEqual(
            96, get_item(self.housing_age_frame,
                         self.mgra_label, 2,
                         self.single_family_labels.total_units)
        )
        self.assertAlmostEqual(0.0, get_item(
            self.housing_age_frame, self.mgra_label, 2,
            self.single_family_labels.proportion_old))

        update_units(self.housing_age_frame, 2, -2, self.single_family_labels)
        self.assertAlmostEqual(
            2/94,
            get_item(self.housing_age_frame,
                     self.mgra_label, 2,
                     self.single_family_labels.proportion_new)
        )
