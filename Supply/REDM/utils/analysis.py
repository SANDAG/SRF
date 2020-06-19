import matplotlib.pyplot as plt
import os
import pandas
import sys

from utils.constants import VACANT_ACRES, MGRA, \
    product_type_unit_size_labels, non_residential_jobs_per_unit_labels


def plot_column(column, output_dir='data/output', image_name='plot.png'):
    column.plot(x=column.index, y=column.values)
    plt.savefig(os.path.join(output_dir, image_name))
    plt.close()


def plot_total_acres(mgra_dataframe, output_dir):
    mgra_dataframe.plot.scatter(x=MGRA, y='total_acres')
    plt.savefig(os.path.join(output_dir, 'plot.png'))
    plt.close()


def plot_nonzero(filename, column_name):
    frame = pandas.read_csv(filename)
    column = frame[column_name]
    plot_column(column[column != 0])


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


def count_zeros(column):
    return column.isin([0]).sum()


# TODO: plot new units
def count_new_units(before, after, product_type):
    """
    returns: series with the amount of new units of that product type
    (after - before)
    """
    new_construction = after[product_type] - before[product_type]
    return new_construction


def average_x_per_y(frame, x, y, product_type):
    # drop zeros
    frame = frame.loc[frame[x] != 0]
    frame = frame.loc[frame[y] != 0]
    result = (frame[x] / frame[y]).mean()
    print('{} average {} per {} = {}'.format(
        product_type, x, y, result))


def average_unit_square_footage(filename, product_type):
    frame = pandas.read_csv(filename)
    total_sqft, total_units = product_type_unit_size_labels(product_type)
    average_x_per_y(frame, total_sqft, total_units, product_type)


def average_jobs_per_unit(filename, product_type):
    frame = pandas.read_csv(filename)
    jobs, units = non_residential_jobs_per_unit_labels(product_type)
    average_x_per_y(frame, jobs, units, product_type)


def print_usage():
    print('useful sanity checks and quick data evaluation')
    print('usage:\nsummarize\nsum ...\nvacancy ...\ncolplot ...',
          '\nunit_size ...\njobs_per_unit')


def run():
    args = sys.argv
    if args[1] == 'summarize':
        if len(args) == 3:
            analyze_mgra(args[2], None)
        elif len(args) == 4:
            analyze_mgra(args[2], args[3])
        else:
            print('usage: summarize filename')
    elif args[1] == 'sum':
        if len(args) == 4:
            sum_column(args[2], args[3])
        else:
            print('usage: sum data/mgra.csv column_name')
    elif args[1] == 'vacancy':
        if len(args) == 5:
            check_vacancy_rates(args[2], args[3], args[4])
        else:
            print('usage: vacancy filename total_units_column '
                  'occupied_units_column')
    elif args[1] == 'colplot':
        if len(args) == 4:
            plot_nonzero(args[2], args[3])
        else:
            print('usage: colplot filename column_name')
    elif args[1] == 'unit_sqft':
        if len(args) == 4:
            average_unit_square_footage(args[2], args[3])
        else:
            print('usage: unit_sqft filename product_type')
    elif args[1] == 'jobs_per_unit':
        if len(args) == 4:
            average_jobs_per_unit(args[2], args[3])
        else:
            print('usage: jobs_per_unit filename product_type')
    else:
        print_usage()


# run as module: path/to/REDM $ python -m utils.analysis ...
if __name__ == "__main__":
    if len(sys.argv) > 1:
        run()
    else:
        print_usage()
