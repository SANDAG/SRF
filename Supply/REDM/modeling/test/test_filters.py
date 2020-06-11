import unittest

import pandas

from modeling.filters import max_new_units_to_meet_vacancy, filter_by_vacancy
# filter_by_profitability, filter_by_vacancy, \
# filter_redevelopment
from utils.constants import SINGLE_FAMILY_HOUSING_UNITS, \
    SINGLE_FAMILY_HOUSEHOLDS


class TestFilters(unittest.TestCase):
    def setUp(self):
        self.mgras = pandas.read_csv('test_data/contrived_MGRA.csv')
        self.max_vacancy = 0.1

        return super().setUp()

    def test_max_new_units_to_meet_vacancy(self):
        new_units = max_new_units_to_meet_vacancy(
            self.mgras,
            SINGLE_FAMILY_HOUSING_UNITS, SINGLE_FAMILY_HOUSEHOLDS,
            self.max_vacancy
        )
        self.assertEqual(new_units.iloc[0], -6)
        self.assertGreater(new_units.iloc[1], 0)

    def test_filter_vacancy(self):

        filtered, _ = filter_by_vacancy(
            self.mgras, SINGLE_FAMILY_HOUSING_UNITS, SINGLE_FAMILY_HOUSEHOLDS,
            self.max_vacancy
        )
        self.assertLess(len(filtered), len(self.mgras))
        self.assertEqual(len(filtered), 1)

        high_vacancy = .3
        filtered, _ = filter_by_vacancy(
            self.mgras,
            SINGLE_FAMILY_HOUSING_UNITS, SINGLE_FAMILY_HOUSEHOLDS,
            high_vacancy
        )
        self.assertEqual(3, len(filtered))

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

        # def test_filter_redevelopment(self):
        #     parcels = pandas.read_csv('test_data/mock_parcels.csv')
        #     model_year = 2020
        #     age_to_drop = 20
        #     redevelopment_filtered = filter_redevelopment(
        #         parcels, forecast_year=model_year, min_age=age_to_drop)
        #     assert len(parcels) != len(redevelopment_filtered)
        #     assert len(redevelopment_filtered) == len(
        #           filter_redevelopment(
        #         redevelopment_filtered, forecast_year=model_year,
        #           min_age=age_to_drop))
        #     # assert len(parcels) != len(filter_redevelopment(
        #     # parcels, forecast_year=model_year, min_age=age_to_drop))
