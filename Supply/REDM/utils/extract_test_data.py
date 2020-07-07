from utils.interface import save_to_file
from modeling.filters import filter_all
import pandas

# Run with python -m utils.extract_test_data to select
# mgra_count random MGRA's with some vacant land to test with
mgra_count = 400
dataframe = pandas.read_csv('data/SRF_Input_Base_V4.1.csv')
dataframe = filter_all(dataframe)
sampled = dataframe.sample(n=mgra_count).reset_index(drop=True)
save_to_file(sampled, './test_data', 'random_MGRA.csv')
