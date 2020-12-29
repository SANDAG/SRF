import unittest
import os

import project_code
import aa_settings as ps

class TestSupplyIntegration(unittest.TestCase):
    def test_supply_integration(self):
        working_directory = os.getcwd()

        year=2013
        if year>2012 and ps.run_supply:
            project_code.before_aa(year, ps=ps)
        self.assertEqual(working_directory, os.getcwd())
        expected_filepath = str(year) + '/FloorspaceO.csv'
        self.assertTrue(os.path.isfile(expected_filepath))
        os.remove(expected_filepath)
        self.assertFalse(os.path.isfile(expected_filepath))
