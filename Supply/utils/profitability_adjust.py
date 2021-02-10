import os
import logging
import pandas

from utils.interface import save_to_file
from utils.access_labels import mgra_labels

MGRA_COUNT = 23002


def make_profitability_file():
    frame = pandas.DataFrame({
        'mgra': [i+1 for i in range(MGRA_COUNT)],
        'adjustment': [0 for _ in range(MGRA_COUNT)]
    })
    save_to_file(frame, 'data', 'profitability.csv', force=True)


def adjust_profitability(mgra_frame):
    profitability_adjustment_frame = load_profitability_adjust()
    mgra_frame[
        mgra_labels.LAND_COST_PER_ACRE
    ] += profitability_adjustment_frame['adjustment']


def load_profitability_adjust():
    path = 'data/profitability.csv'
    # will profitability be added to database?
    # if there isn't one, make one.
    if os.path.isfile(path):
        return pandas.read_csv(path)
    else:
        logging.info(
            'couldn\'t find profitability adjustment csv, ' +
            'creating a blank one')
        make_profitability_file()
        return pandas.read_csv(path)


if __name__ == "__main__":
    # use this to reset profitability file as needed
    # usage: `python -m utils.profitability_adjust`
    make_profitability_file()
