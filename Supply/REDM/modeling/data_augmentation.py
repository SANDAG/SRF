import numpy as np
from utils.interface import save_to_file


def replace_zeros_with_sliding_average(dataframe, column_name, window_size=25):
    save_to_file(dataframe[column_name],
                 'data/output', 'prev_prices.csv')
    # TODO: only work with applicable mgras instead of the whole file

    # replace zeros with nans so they can be ignored, then replaced by
    # rolling window
    dataframe[column_name] = dataframe[column_name].replace(
        {0: np.nan})
    save_to_file(dataframe[column_name],
                 'data/output', 'nan_prices.csv')
    # FIXME: averaging everything instead of just nans.
    dataframe[column_name].update(
        dataframe[column_name].rolling(
            window_size, center=True, min_periods=3).mean()
    )
    save_to_file(dataframe[column_name],
                 'data/output', 'new_prices.csv')
