import unittest
import pandas

from utils.pandas_shortcuts import normalize


class TestPandasShortcuts(unittest.TestCase):
    def test_normalize(self):
        collection = pandas.Series([10, 20, 30, 40])
        expected_result = pandas.Series([0.1, 0.2, 0.3, 0.4])
        self.assertTrue(expected_result.equals(normalize(collection)))
