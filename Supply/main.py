import pandas
from tqdm import tqdm
import logging

from modeling.develop import develop
from utils.interface import \
    load_parameters, empty_folder, save_to_file, open_dbf
import utils.config as config
from scheduled_development import run as add_scheduled_development


def run(mgra_dataframe, planned_sites):
    output_dir = config.parameters['output_directory']
    simulation_years = config.parameters['simulation_years']
    simulation_begin = config.parameters['simulation_begin']

    steps_per_year = 8
    progress = tqdm(desc='progress', total=simulation_years *
                    steps_per_year, position=0)

    for i in range(simulation_years):
        forecast_year = simulation_begin + i + 1
        progress.set_description(
            'starting year {} adding scheduled development'.format(i+1))

        # add scheduled development
        add_scheduled_development(mgra_dataframe, planned_sites, output_dir)
        progress.update()
        # develop enough land to meet demand for this year.
        mgra_dataframe, progress = develop(mgra_dataframe, progress)
        if mgra_dataframe is None:
            print('program terminated, {} years were completed'.format(i))
            return
        progress.update()

        progress.set_description('saving year {}'.format(i+1))
        save_to_file(mgra_dataframe, output_dir, 'year{}_{}.csv'.format(
            i + 1, forecast_year))
        progress.update()
    progress.close()
    return


if __name__ == "__main__":
    # load parameters
    config.parameters = load_parameters('parameters.yaml')

    if config.parameters is not None:
        # prep output directory
        output_dir = config.parameters['output_directory']
        empty_folder(output_dir)
        save_to_file(config.parameters, output_dir, 'last_run_parameters.yaml')
        # configure logging level
        if config.parameters['debug']:
            logging.basicConfig(level=logging.DEBUG)
        # load dataframe
        mgra_dataframe = pandas.read_csv(config.parameters['input_filename'])
        planned_sites = open_dbf(config.parameters['sites_filename'])

        run(mgra_dataframe, planned_sites)
    else:
        print('could not load parameters, exiting')