import unittest
import pandas
import logging

from utils.aa_floorspace_update import combine_frames, luz_squarefootages, \
    luz_subtype_ratios, calculate_residential_floorspace, \
    add_floorspace_entry, update_floorspace

output_row_id_label = 'LUZ'


class TestAAFloorspaceUpdate(unittest.TestCase):

    def setUp(self):
        self.simple_mgra_frame = pandas.DataFrame({
            'LUZ': [1, 1, 1],
            'SqFt_SF': [200, 500, 500],
            'SqFt_MF': [100, 200, 300]
        })

    def test_combine_frames(self):
        frame_1 = pandas.DataFrame({
            output_row_id_label: [1, 2],
            'Commodity': ['single_family', 's'],
            'Quantity': [2, 1]
        })
        frame_2 = pandas.DataFrame({
            output_row_id_label: [1, 2, 3],
            'Commodity': ['single_family', 's', 's'],
            'Quantity': [2, 2, 1]
        })
        expected_answer = pandas.DataFrame({
            output_row_id_label: [1, 2, 3],
            'Commodity': ['single_family', 's', 's'],
            'Quantity': [2, 1, 1]
        })

        answer = combine_frames(frame_1, frame_2)
        logging.debug('testing {} rows'.format(len(answer)))
        for i in range(len(expected_answer)):
            logging.debug(answer.iloc[i])
            self.assertTrue(expected_answer.iloc[i].equals(answer.iloc[i]))
        empty_frame = pandas.DataFrame({})
        self.assertEqual(len(combine_frames(frame_1, empty_frame)), 2)

    def test_luz_squarefootages(self):
        mgra_frame = pandas.DataFrame({
            'LUZ': [1, 1, 1, 2, 2],
            'SqFt_SF': [200, 500, 500, 100, 0],
            'SqFt_MF': [100, 200, 300, 300, 0]
        })
        label = 'SqFt_SF'
        expected_answer = {1: 1200, 2: 100}
        self.assertEqual(
            expected_answer, luz_squarefootages(mgra_frame, label))
        multi_family_label = 'SqFt_MF'
        expected_answer = {1: 600, 2: 300}
        self.assertEqual(expected_answer, luz_squarefootages(
            mgra_frame, multi_family_label))

        # ... also test with self.simple_mgra_frame

    def test_luz_subtype_ratios(self):
        floorspace = pandas.DataFrame({
            output_row_id_label: [1, 2],
            'Commodity': ['s', 'm'],
            'Quantity': [100, 200]
        })
        subtypes = ['s']
        self.assertEqual(1, len(luz_subtype_ratios(floorspace, subtypes)))

    def test_add_floorspace_entry(self):
        # basic test with 100% of one product subtype
        single_family_commodity = "Single Family Detached Residential Economy"
        entry = (1, 100)
        # equal to the luz_subtype_ratios output
        ratios = {1: {single_family_commodity: 100}}
        subtypes = {"Single Family Detached Residential Economy": 1.0}
        output = []
        # an array of aa_luz_export.create_row return values
        expected_output = [{output_row_id_label: 1,
                            "Commodity": single_family_commodity,
                            "Quantity": 100}]

        # modifies output in place
        add_floorspace_entry(entry, ratios, output, subtypes)
        self.assertEqual(expected_output, output)
        # tests with ratios
        entry = (1, 100)
        single_family_subtype_2 = "Single Family Detached Residential Luxury"
        ratios = {1: {
            single_family_commodity: 100,
            single_family_subtype_2: 100
        }}
        output = []
        expected_output = [
            {output_row_id_label: 1,
             "Commodity": single_family_commodity,
             "Quantity": 50.0},
            {output_row_id_label: 1,
             "Commodity": single_family_subtype_2,
             "Quantity": 50.0}
        ]
        add_floorspace_entry(entry, ratios, output, subtypes)
        self.assertEqual(expected_output, output)

    def test_calculate_residential_floorspace(self):
        mgra_frame = self.simple_mgra_frame
        floorspace_frame = pandas.DataFrame({
            output_row_id_label: [1, 2, 1],
            'Commodity': [
                "Single Family Detached Residential Economy",
                "Single Family Detached Residential Economy",
                "Multi-Family Residential Economy"
            ],
            'Quantity': [3000, 4000, 100]
        })

        expected_answer = pandas.DataFrame({
            output_row_id_label: [1, 1],
            'Commodity': [
                'Single Family Detached Residential Economy',
                'Multi-Family Residential Economy'],
            'Quantity': [1200.0, 600.0]
        })
        answer = calculate_residential_floorspace(mgra_frame, floorspace_frame)
        self.assertTrue(expected_answer.equals(answer))
#         luz_10013 = pandas.DataFrame({
#             10013,Single Family Attached Residential Luxury,1.2
# 10013,Single Family Detached Residential Economy,80553.42004
# 10013,Single Family Detached Residential Luxury,16315.71205
# 10013,Spaced Rural Residential Economy,11041.03894
# 10013,Spaced Rural Residential Luxury,2121.01975
#         })

# uncomment for integration testing (uses database)
    # def test_update_floorspace(self):
    #     update_floorspace(pandas.read_csv('test_data/random_MGRA.csv'), 2013)

# TODO:
# add the cases where:
# there are no floorspace entries for a subtype on an luz, but there needs to
# be a ratio for allocating to the subtypes
