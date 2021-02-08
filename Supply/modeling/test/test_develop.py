import unittest
import pandas

from modeling.develop import buildable_units
# develop, choose_candidate
# from modeling.candidates import create_candidate_set
from utils.access_labels import ProductTypeLabels


class TestDevelop(unittest.TestCase):
    def setUp(self):
        self.candidate = pandas.DataFrame({
            "vacancy_cap": [20],
            "vac": [6.0],
            "vac_sf": [6.0],
            "redev_mh_s": [None],
            "redev_ag_s": [None],
            "redev_emp1": [None],
            "redev_ag_r": [None],
            "redev_ag_l": [None],
            "infill_sf": [None],
        })
        self.product_type_labels = ProductTypeLabels('single_family')

        self.short_mgras = pandas.read_csv('test_data/random_MGRA.csv')
        # self.test_mgras = pandas.read_csv('data/SRF_Input_Base_V4.1.csv')

        return super().setUp()

    def test_buildable_units(self):
        self.assertEqual(
            20,
            buildable_units(
                self.candidate,
                self.product_type_labels,
                100)
        )

    # def test_choose_candidate(self):
    #     candidates = create_candidate_set(self.short_mgras)
    #     max_units = 10
    #     result = choose_candidate(
    #         candidates, self.short_mgras,
    #         self.product_type_labels, max_units)
    #     self.assertIsNotNone(result)

    # def test_develop(self):
    #     self.assertIsNotNone(develop(self.short_mgras))
