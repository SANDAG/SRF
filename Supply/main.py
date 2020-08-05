import pandas
import logging

from scheduled_development import run as add_scheduled_development
from modeling.develop import develop
from utils.interface import \
    load_parameters, empty_folder, save_to_file, open_dbf
from utils.aa_export import export_aa
import utils.config as config


def run(mgra_dataframe, planned_sites):
    output_dir = config.parameters['output_directory']
    simulation_years = config.parameters['simulation_years']
    simulation_begin = config.parameters['simulation_begin']

    for i in range(simulation_years):
        forecast_year = simulation_begin + i + 1

        print('adding scheduled development:')
        add_scheduled_development(
            mgra_dataframe, planned_sites, output_dir,
            starting_year=simulation_begin + i)
        print('developing to meet remaining demand:')
        mgra_dataframe = develop(mgra_dataframe)
        if mgra_dataframe is None:
            print('program terminated, {} years were completed'.format(i))
            return

        print('saving year{}_{}.csv ... '.format(i + 1, forecast_year))
        save_to_file(mgra_dataframe, output_dir, 'year{}_{}.csv'.format(
            i + 1, forecast_year))
        print('saved')
        print('creating AA commodity export file ...')
        export_aa(mgra_dataframe)
        print('Done')
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
