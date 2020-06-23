import numpy as np

from utils.interface import save_to_file
from utils.constants import OFFICE_PRICE, COMMERCIAL_PRICE, INDUSTRIAL_PRICE
import utils.config as config


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


def add_non_residential_average_prices(dataframe):
    # This works, but we will just use the parameters in the profitability
    # filter and leave this unused for now
    dataframe.loc[dataframe[OFFICE_PRICE] == 0, OFFICE_PRICE] = \
        config.parameters['office_average_price']
    dataframe.loc[dataframe[COMMERCIAL_PRICE] == 0, COMMERCIAL_PRICE] = \
        config.parameters['commercial_average_price']
    dataframe.loc[dataframe[INDUSTRIAL_PRICE] == 0, INDUSTRIAL_PRICE] = \
        config.parameters['industrial_average_price']
    save_to_file(dataframe, 'data/output', 'new_non_res_prices.csv')
    return dataframe
