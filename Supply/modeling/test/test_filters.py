import unittest
import pandas

from modeling.filters import filter_by_vacancy, generic_filter, \
    construction_multiplier, filter_by_profitability, acreage_available, \
    filter_product_type, apply_filters
from modeling.candidates import create_candidate_set
from utils.access_labels import ProductTypeLabels, mgra_labels


class TestFilters(unittest.TestCase):
    def setUp(self):
        self.mgras = pandas.read_csv('test_data/random_MGRA.csv')
        self.max_vacancy = 0.06
        self.product_type_labels = ProductTypeLabels('single_family')
        self.combined_frame = pandas.DataFrame(
            {
                "MGRA": [1, 2, 3, 4, 5, 6, 7],
                "vac_sf": [2.0, None,  None, None, None, None, None],
                "redev_mh_s": [None,  None, None, None, None, None, 2.0],
                "redev_ag_s": [None,  None, None, None, None, 2.0, None],
                "redev_emp1": [None,  None, None, None, 2.0, None, None],
                "redev_ag_r": [None,  None, None, 2.0, None, None, None],
                "redev_ag_l": [None,  None, 2.0, None, None, None, None],
                "infill_sf": [None, 2.0,  None, None, None, None, None],
                mgra_labels.LAND_COST_PER_ACRE: [
                    10000, 200, 300, 400, 500, 600, 700],
                self.product_type_labels.price: [
                    100, 200, 300, 400, 500, 600, 700],
                self.product_type_labels.capacity: [
                    100, 200, 300, 400, 500, 600, 700],
                self.product_type_labels.total_units: [
                    50, 100, 200, 300, 400, 500, 600
                ],
                "hs_sf": [200, 235, 460, 563, 0, 1000, 1000],
                "hh_sf": [200, 100, 398, 543, 0, 970, 945],
                "units_available": [
                    100, 100, 29, 0, 218, 300, 200]
            }
        )
        self.vacancy_frame = pandas.DataFrame(
            {
                "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                "hs_sf": [200, 235, 460, 563, 49, 125, 0, 145, 58, 1000, 1000],
                "hh_sf": [200, 100, 398, 543, 49, 125, 0, 129, 39, 970, 945],
                "units_available": [
                    100, 100, 29, 45, 0, 218, 1230, 0, 200, 300, 200],
            }
        )
        self.profitability_frame = pandas.DataFrame(
            {
                "MGRA": [1, 2, 3, 4, 5, 6, 7],
                "vac_sf": [2.0, None,  None, None, None, None, None],
                "redev_mh_s": [None,  None, None, None, None, None, 2.0],
                "redev_ag_s": [None,  None, None, None, None, 2.0, None],
                "redev_emp1": [None,  None, None, None, 2.0, None, None],
                "redev_ag_r": [None,  None, None, 2.0, None, None, None],
                "redev_ag_l": [None,  None, 2.0, None, None, None, None],
                "infill_sf": [None, 2.0,  None, None, None, None, None],
                mgra_labels.LAND_COST_PER_ACRE: [
                    10000, 200, 300, 400, 500, 600, 700],
                self.product_type_labels.price: [
                    100, 200, 300, 400, 500, 600, 700]
            }
        )
        return super().setUp()

    def membership_check(self, items, collection, excluded=False):
        for item in items:
            if excluded:
                self.assertNotIn(item, list(collection))
            else:
                self.assertIn(item, list(collection))

    def test_generic_filter(self):

        self.nan_frame = pandas.DataFrame(
            {
                "id": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "tastiness": [200, 235, 460, 563, None, 125, 0, 145, 58],
                "moxy": [4.4, 5.2, 2.1, 9.4, 0.0, 0.0, 3.5, 9.3, 7.2],
                "hyperdrive": [1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, None, 1.0],
                "delicacy": [32, 46, 74, 29, 16, 47, 50, 20, 42],
                "pulp_level": [
                    56.0, 21.0, 10.0, 99.0, 43.0, 39.0, 54.0, 15.0, 63.1]
            }
        )
        # print(self.nan_frame)
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

    def test_apply_filters(self):
        self.assertIsNotNone(apply_filters(
            self.combined_frame, self.product_type_labels))
        # uncomment to test behavior on actual candidates
        # candidates = create_candidate_set(self.mgras)
        # self.assertIsNotNone(apply_filters(
        #     candidates, self.product_type_labels))

    def test_acreage_available(self):
        # adding coverage
        self.assertIsNotNone(acreage_available(
            self.profitability_frame, self.product_type_labels))

    def test_filter_product_type(self):
        self.assertIsNotNone(filter_product_type(
            self.combined_frame, self.product_type_labels))

    def test_filter_vacancy(self):
        self.vacancy_frame = pandas.DataFrame(
            {
                "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                "hs_sf": [200, 235, 460, 563, 49, 125, 0, 145, 58, 1000, 1000],
                "hh_sf": [200, 100, 398, 543, 49, 125, 0, 129, 39, 970, 945],
                "units_available": [
                    100, 100, 29, 45, 0, 218, 1230, 0, 200, 300, 200],
            }
        )
        filtered = filter_by_vacancy(
            self.vacancy_frame, self.product_type_labels,
            target_vacancy_rate=self.max_vacancy
        )

        self.assertLess(len(filtered), len(self.vacancy_frame))
        # check that less MGRA's are filtered for a very high rate
        high_vacancy = .3
        previous_size = len(filtered)
        filtered = filter_by_vacancy(
            self.vacancy_frame, self.product_type_labels,
            target_vacancy_rate=high_vacancy
        )
        self.assertLess(previous_size, len(filtered))

        # coverage
        filtered = filter_by_vacancy(
            self.vacancy_frame, self.product_type_labels
        )

    def test_filter_by_profitability(self):
        # TODO: check filtering accuracy
        # Just adding coverage for now
        self.assertIsNotNone(filter_by_profitability(
            self.profitability_frame, self.product_type_labels))

    def test_construction_multiplier(self):
        # multipliers must match test_parameters
        expected_output = pandas.Series([1, 1.1, 1.25, 1.25, 1.25, 1.25, 1.25])

        output = construction_multiplier(
            self.profitability_frame,
            self.product_type_labels
        )
        self.assertTrue(expected_output.equals(output))
