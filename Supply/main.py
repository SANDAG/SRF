import os.path
import pandas
import logging

from scheduled_development import run as add_scheduled_development
from modeling.develop import develop
from utils.interface import \
    load_parameters, empty_folder, save_to_file, open_dbf
from utils.aa_luz_export import export_luz_data, CROSSWALK_FILEPATH
import utils.config as config
from utils.data_prep import create_version_4point1


def run(mgra_dataframe, planned_sites):
    output_dir = config.parameters['output_directory']
    simulation_years = config.parameters['simulation_years']
    simulation_begin = config.parameters['simulation_begin']

    for i in range(simulation_years):
        forecast_year = simulation_begin + i + 1
        if planned_sites is not None:
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
        if os.path.isfile(CROSSWALK_FILEPATH):
            export_luz_data(mgra_dataframe)
        else:
            print('missing crosswalk file: \"{}\". Skipping aa export'.format(
                CROSSWALK_FILEPATH))
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

        # prep input
        if not os.path.exists('data/SRF_Input_Base_V4.1.csv'):
            create_version_4point1()
        # load dataframe
        mgra_dataframe = pandas.read_csv(config.parameters['input_filename'])
        # load scheduled development if a file is available
        scheduled_development_filepath = config.parameters['sites_filename']
        if os.path.isfile(scheduled_development_filepath):
            planned_sites = open_dbf(scheduled_development_filepath)
        else:
            print('no scheduled development file found (\"{}\"), skipping'
                  .format(scheduled_development_filepath))
            planned_sites = None
        # start simulation
        run(mgra_dataframe, planned_sites)
    else:
        print('could not load parameters, exiting')
