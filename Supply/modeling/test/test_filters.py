import unittest
import pandas

from modeling.filters import filter_by_vacancy, generic_filter, \
    construction_multiplier
from utils.access_labels import ProductTypeLabels


class TestFilters(unittest.TestCase):
    def setUp(self):
        self.mgras = pandas.read_csv('test_data/random_MGRA.csv')
        self.max_vacancy = 0.06
        self.product_type_labels = ProductTypeLabels()
        return super().setUp()

    def membership_check(self, items, collection, excluded=False):
        for item in items:
            if excluded:
                self.assertNotIn(item, list(collection))
            else:
                self.assertIn(item, list(collection))

    def test_generic_filter(self):
        self.nan_frame = pandas.read_csv('test_data/filtering/frame_nans.csv')

        self.ids_to_keep = [1, 2, 9]
        self.ids_with_nans = [5, 8]
        self.ids_with_zeros = [3, 4, 5, 6, 7]

        self.membership_check(self.ids_to_keep, self.nan_frame['id'])
        # check if both zeros and NaNs can be removed
        self.filtered_both = generic_filter(
            self.nan_frame, self.nan_frame.columns)
        self.membership_check(self.ids_to_keep, self.filtered_both['id'])
        self.membership_check(self.ids_with_nans,
                              self.filtered_both['id'], excluded=True)
        self.membership_check(self.ids_with_zeros,
                              self.filtered_both['id'], excluded=True)
        # check if just zeros can be removed
        # self.filtered_zeros = generic_filter(
        #     self.nan_frame, self.nan_frame.columns, filter_nans=False)
        # self.membership_check(self.ids_with_nans, self.filtered_zeros['id'])

    def test_filter_vacancy(self):
        filtered, max_new_units = filter_by_vacancy(
            self.mgras, self.product_type_labels,
            target_vacancy_rate=self.max_vacancy
        )
        self.assertEqual(len(filtered), len(max_new_units))
        self.assertLess(len(filtered), len(self.mgras))
        # check that less MGRA's are filtered for a very high rate
        high_vacancy = .3
        previous_size = len(filtered)
        filtered, _ = filter_by_vacancy(
            self.mgras, self.product_type_labels,
            target_vacancy_rate=high_vacancy
        )
        self.assertLess(previous_size, len(filtered))

    # def test_filter_profitability(self):
    #     parcels = pandas.read_csv('test_data/mock_parcels.csv')
    #     # test for dropping unprofitable parcels
    #     #filtered = filter_by_profitability(parcels)
    #     #assert len(parcels) != len(filtered)
    #     filtered_parcels = filter_by_profitability(parcels)
    #     assert len(parcels) != len(filtered_parcels)
    #     assert len(filtered_parcels) == len(
    #         filter_by_profitability(filtered_parcels))

    def test_construction_multiplier(self):
        self.single_family_candidates = pandas.read_csv(
            'test_data/filtering/mock_single_family_candidates.csv')
        # csv multipliers must match test_parameters
        self.expected_output = pandas.read_csv(
            'test_data/filtering/expected_profit_multipliers.csv')
        self.expected_output = self.expected_output['series']
        output = construction_multiplier(
            self.single_family_candidates,
            ProductTypeLabels('single_family')
        )
        self.assertTrue(self.expected_output.equals(output))
