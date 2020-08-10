import unittest
import pandas

from modeling.filters import filter_by_vacancy
from utils.access_labels import ProductTypeLabels


class TestFilters(unittest.TestCase):
    def setUp(self):
        self.mgras = pandas.read_csv('test_data/random_MGRA.csv')
        self.max_vacancy = 0.06
        self.product_type_labels = ProductTypeLabels()
        return super().setUp()

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

        # def test_filter_vacancy(self):
        #     parcels = pandas.read_csv('test_data/mock_parcels.csv')
        #     max_vacancy_rate = 0.07
        #     vacancy_filtered = filter_by_vacancy(
        #         parcels, target_vacancy_rate=max_vacancy_rate)
        #     assert len(parcels) != len(vacancy_filtered)
        #     assert len(vacancy_filtered) == len(filter_by_vacancy(
        #         vacancy_filtered, target_vacancy_rate=max_vacancy_rate))
        #     # assert len(parcels) != len(filter_by_vacancy(
        #     # parcels, target_vacancy_rate=max_vacancy_rate))
