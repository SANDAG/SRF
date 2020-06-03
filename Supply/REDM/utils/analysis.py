import matplotlib.pyplot as plt
import os
import pandas
import sys


def plot_total_acres(mgra_dataframe, output_dir):
    mgra_dataframe.plot.scatter(x='mgra_ID', y='total_acres')
    plt.savefig(
        os.path.join(output_dir, 'plot.png'))
    plt.close()


def analyze_mgra(mgra_dataframe, output_dir):
    print(mgra_dataframe.dtypes)
    print(mgra_dataframe.memory_usage(deep=True))
    print('single frame memory usage: {}MB'.format(
        mgra_dataframe.memory_usage(deep=True).sum()/100000))
    vacant_count = len(mgra_dataframe[mgra_dataframe['total_vacant'] > 0.5])

    print('MGRA\'s with 1/2 acre or more vacant: {}/{}'.format(
        vacant_count, len(mgra_dataframe)))

    print('pandas description')
    print(mgra_dataframe.describe())

    # TODO: Add additional interesting data visualizations
    plot_total_acres(mgra_dataframe, output_dir)


def sum_column(filename, column_name):
    dataframe = pandas.read_csv(filename)
    print('{} sum: {}'.format(column_name, dataframe[column_name].sum()))


# TODO: plot new units

def count_new_units(before, after, product_type):
    """
    returns: series with the amount of new units of that product type
    (after - before)
    """
    new_construction = after[product_type] - before[product_type]
    return new_construction


if __name__ == "__main__":
    if sys.argv[1] == 'sum' and len(sys.argv) == 4:
        sum_column(sys.argv[2], sys.argv[3])
    else:
        print('usage: sum data/mgra.csv column_name')
