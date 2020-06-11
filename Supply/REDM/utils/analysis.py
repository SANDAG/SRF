import matplotlib.pyplot as plt
import os
import pandas
import sys

from constants import VACANT_ACRES


def plot_total_acres(mgra_dataframe, output_dir):
    mgra_dataframe.plot.scatter(x='mgra_ID', y='total_acres')
    plt.savefig(
        os.path.join(output_dir, 'plot.png'))
    plt.close()


def analyze_mgra(filename, output_dir):
    mgra_dataframe = pandas.read_csv(filename)
    print(mgra_dataframe.dtypes)
    print(mgra_dataframe.memory_usage(deep=True))
    print('single frame memory usage: {}MB'.format(
        mgra_dataframe.memory_usage(deep=True).sum()/100000))
    vacant_count = len(mgra_dataframe[mgra_dataframe[VACANT_ACRES] > 0.5])

    print('MGRA\'s with 1/2 acre or more vacant: {}/{}'.format(
        vacant_count, len(mgra_dataframe)))

    print('pandas description')
    print(mgra_dataframe.describe())

    # TODO: Add additional interesting data visualizations
    if output_dir is not None:
        plot_total_acres(mgra_dataframe, output_dir)


def check_vacancy_rates(filename, total_units, occupied_units):
    frame = pandas.read_csv(filename)
    frame = frame[frame[total_units] > 0]
    frame = frame[frame[occupied_units] > 0]

    rates = (frame[total_units] - frame[occupied_units]) / frame[total_units]
    print(
        'vacancy rates description from frame with {} rows'.format(len(frame))
    )
    print(rates.describe())

    print('rows with more occupied than total units(!)')
    backwards_rates = frame[rates < 0]
    print(backwards_rates)

    target_vacancy = 0.06
    available_count = len(frame[rates < target_vacancy])
    print('MGRA\'s below target vacancy rate of {}: {} out of {}'.format(
        target_vacancy, available_count, len(frame)))


def sum_column(filename, column_name):
    dataframe = pandas.read_csv(filename)
    print(
        '{} ({} rows) sum: {}'.format(
            column_name,
            len(dataframe), dataframe[column_name].sum())
    )


# TODO: plot new units

def count_new_units(before, after, product_type):
    """
    returns: series with the amount of new units of that product type
    (after - before)
    """
    new_construction = after[product_type] - before[product_type]
    return new_construction


def print_usage():
    print('useful sanity checks and quick data evaluation')
    print('usage: summarize ; sum ... ; vacancy...')


def run():
    if sys.argv[1] == 'summarize':
        if len(sys.argv) == 3:
            analyze_mgra(sys.argv[2], None)
        elif len(sys.argv) == 4:
            analyze_mgra(sys.argv[2], sys.argv[3])
        else:
            print('usage: summarize filename')
    elif sys.argv[1] == 'sum':
        if len(sys.argv) == 4:
            sum_column(sys.argv[2], sys.argv[3])
        else:
            print('usage: sum data/mgra.csv column_name')
    elif sys.argv[1] == 'vacancy':
        if len(sys.argv) == 5:
            check_vacancy_rates(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            print('usage: vacancy filename total_units_column occupied_units_column')
    else:
        print_usage()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run()
    else:
        print_usage()
