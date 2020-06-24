import numpy as np

from utils.constants import OFFICE_PRICE, COMMERCIAL_PRICE, INDUSTRIAL_PRICE, \
    SINGLE_FAMILY_PRICE, MULTI_FAMILY_PRICE
import utils.config as config


def fill_in_price_data(dataframe):
    dataframe = replace_zeros_with_sliding_average(
        dataframe, SINGLE_FAMILY_PRICE)
    dataframe = replace_zeros_with_sliding_average(
        dataframe, MULTI_FAMILY_PRICE)
    return dataframe


def replace_zeros_with_sliding_average(dataframe, column_name, window_size=25):
    # TODO: only work with applicable mgras instead of the whole file

    # replace zeros with nans so they can be replaced by
    # rolling window
    dataframe[column_name] = dataframe[column_name].replace(
        {0: np.nan})

    dataframe[column_name] = dataframe[column_name].fillna(
        dataframe[column_name].rolling(75, min_periods=1).mean())
    # if there weren't any values to average nearby, it should be just as
    # accurate to fill with the average across the entire column.
    dataframe[column_name] = dataframe[column_name].fillna(
        dataframe[column_name].mean())

    return dataframe


def add_non_residential_average_prices(dataframe):
    # This works, but we will just use the parameters in the profitability
    # filter and leave this unused for now
    dataframe.loc[dataframe[OFFICE_PRICE] == 0, OFFICE_PRICE] = \
        config.parameters['office_average_price']
    dataframe.loc[dataframe[COMMERCIAL_PRICE] == 0, COMMERCIAL_PRICE] = \
        config.parameters['commercial_average_price']
    dataframe.loc[dataframe[INDUSTRIAL_PRICE] == 0, INDUSTRIAL_PRICE] = \
        config.parameters['industrial_average_price']
    return dataframe
