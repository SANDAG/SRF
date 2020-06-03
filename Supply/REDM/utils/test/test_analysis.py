import unittest
import pandas

from utils.analysis import count_new_units
from utils.constants import SINGLE_FAMILY_HOUSING_UNITS


class TestAnalysis(unittest.TestCase):
    def setUp(self):
        self.before = pandas.read_csv('test_data/output/year1_2021.csv')
        self.after = pandas.read_csv('test_data/output/year2_2022.csv')

    def test_count_new_units(self):
        self.assertNotEqual(count_new_units(
            self.before, self.after, SINGLE_FAMILY_HOUSING_UNITS).sum(), 0)
        return
