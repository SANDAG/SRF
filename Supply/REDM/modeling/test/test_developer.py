import unittest

import pandas

from modeling.developer import develop, update_housing
from utils.interface import load_parameters
import utils.config as config
from utils.constants import MGRA, HOUSING_UNITS, SINGLE_FAMILY_HOUSING_UNITS, \
    SINGLE_FAMILY_DEVELOPED_ACRES, SINGLE_FAMILY_VACANT_ACRES, \
    MULTI_FAMILY_DEVELOPED_ACRES, MULTI_FAMILY_VACANT_ACRES, \
    OFFICE_DEVELOPED_ACRES, OFFICE_VACANT_ACRES, \
    INDUSTRIAL_DEVELOPED_ACRES, INDUSTRIAL_VACANT_ACRES, \
    COMMERCIAL_DEVELOPED_ACRES, COMMERCIAL_VACANT_ACRES, \
    DEVELOPED_ACRES, VACANT_ACRES


class TestDeveloper(unittest.TestCase):
    def setUp(self):
        config.parameters = load_parameters('test_parameters.yaml')
        self.assertIsNotNone(config.parameters)
        self.test_frame = pandas.read_csv('test_data/contrived_MGRA.csv')

    def test_update_housing(self):
        total_housing_before = self.test_frame[HOUSING_UNITS].sum()
        single_family_units_before = self.test_frame[SINGLE_FAMILY_HOUSING_UNITS].sum(
        )

        mgra_id = self.test_frame.sample()[MGRA].iloc[0]
        units = 1
        self.test_frame = update_housing(
            self.test_frame, mgra_id, units,
            SINGLE_FAMILY_HOUSING_UNITS
        )

        self.assertGreater(
            self.test_frame[HOUSING_UNITS].sum(), total_housing_before
        )
        self.assertGreater(
            self.test_frame[SINGLE_FAMILY_HOUSING_UNITS].sum(),
            single_family_units_before
        )

    def test_develop_overall(self):

        total_developed_before = self.test_frame[DEVELOPED_ACRES].sum()
        total_vacant_before = self.test_frame[VACANT_ACRES].sum()

        # TODO develop modifies in place, is there a way to make this explicit?
        self.test_frame = develop(self.test_frame, self.test_frame)

        self.assertGreater(self.test_frame[DEVELOPED_ACRES].sum(),
                           total_developed_before)
        self.assertLess(self.test_frame[VACANT_ACRES].sum(),
                        total_vacant_before)

    def test_develop_residential(self):
        developed_single_family_before = \
            self.test_frame[SINGLE_FAMILY_DEVELOPED_ACRES].sum()
        vacant_single_family_before = \
            self.test_frame[SINGLE_FAMILY_VACANT_ACRES].sum()

        developed_multi_family_before = \
            self.test_frame[MULTI_FAMILY_DEVELOPED_ACRES].sum()
        vacant_multi_family_before = \
            self.test_frame[MULTI_FAMILY_VACANT_ACRES].sum()

        self.test_frame = develop(self.test_frame, self.test_frame)

        self.assertGreater(self.test_frame[SINGLE_FAMILY_DEVELOPED_ACRES].sum(),
                           developed_single_family_before)
        self.assertLess(self.test_frame[SINGLE_FAMILY_VACANT_ACRES].sum(),
                        vacant_single_family_before)

        self.assertGreater(self.test_frame[MULTI_FAMILY_DEVELOPED_ACRES].sum(),
                           developed_multi_family_before)
        self.assertLess(self.test_frame[MULTI_FAMILY_VACANT_ACRES].sum(),
                        vacant_multi_family_before)

    def test_develop_nonresidential(self):
        developed_industrial_before = \
            self.test_frame[INDUSTRIAL_DEVELOPED_ACRES].sum()
        vacant_industrial_before = self.test_frame[INDUSTRIAL_VACANT_ACRES].sum(
        )

        developed_commercial_before = \
            self.test_frame[COMMERCIAL_DEVELOPED_ACRES].sum()
        vacant_commercial_before = self.test_frame[COMMERCIAL_VACANT_ACRES].sum(
        )

        developed_office_before = self.test_frame[OFFICE_DEVELOPED_ACRES].sum()
        vacant_office_before = self.test_frame[OFFICE_VACANT_ACRES].sum()

        self.test_frame = develop(self.test_frame, self.test_frame)

        self.assertGreater(self.test_frame[INDUSTRIAL_DEVELOPED_ACRES].sum(),
                           developed_industrial_before)
        self.assertLess(self.test_frame[INDUSTRIAL_VACANT_ACRES].sum(),
                        vacant_industrial_before)

        self.assertGreater(self.test_frame[COMMERCIAL_DEVELOPED_ACRES].sum(),
                           developed_commercial_before)
        self.assertLess(self.test_frame[COMMERCIAL_VACANT_ACRES].sum(),
                        vacant_commercial_before)

        self.assertGreater(self.test_frame[OFFICE_DEVELOPED_ACRES].sum(),
                           developed_office_before)
        self.assertLess(self.test_frame[OFFICE_VACANT_ACRES].sum(),
                        vacant_office_before)
