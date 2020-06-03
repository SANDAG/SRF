import unittest
import os


class TestMain(unittest.TestCase):
    def setUp(self):
        pass

    def test_redm_main(self):
        result = os.system('python redm_main.py -t')
        self.assertEqual(result, 0)
