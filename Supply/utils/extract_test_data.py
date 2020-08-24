from utils.interface import save_to_file
from utils.access_labels import mgra_labels
from modeling.filters import generic_filter
import pandas

# Run with python -m utils.extract_test_data to select
# mgra_count random MGRA's with some vacant land to test with
mgra_count = 300
dataframe = pandas.read_csv('data/SRF_Input_Base_V4.1.csv')
dataframe = generic_filter(
    dataframe, [mgra_labels.VACANT_ACRES], filter_nans=False)
sampled = dataframe.sample(n=mgra_count).reset_index(drop=True)
save_to_file(sampled, './test_data', 'random_MGRA.csv')
