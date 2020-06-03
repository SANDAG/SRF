from interface import save_to_file
import pandas

# Run to select mgra_count random MGRA's to test with
mgra_count = 200
dataframe = pandas.read_csv('data/mgra2012.csv')
sampled = dataframe.sample(n=mgra_count).reset_index(drop=True)
save_to_file(sampled, './test_data', 'random_MGRAs.csv')
