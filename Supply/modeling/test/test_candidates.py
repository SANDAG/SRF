import unittest
import pandas

from modeling.candidates import combine_weights


class TestCandidates(unittest.TestCase):
    def setUp(self):
        # self.short_mgras = pandas.read_csv(
        #     'test_data/random_MGRA.csv')
        return super().setUp()

    # def test_create_candidate_set(self):
    #     self.assertIsNotNone(create_candidate_set(self.short_mgras))

    def test_combine_weights(self):
        profitability = pandas.Series([0.9, 0.6, 1.0, 1.1])
        vacancy = pandas.Series([10, 100, 5, 30])
        # coverage
        result = combine_weights(profitability, vacancy)
        # print(result)
        self.assertIsNotNone(result)
