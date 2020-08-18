import os.path
import pandas

from scheduled_development import run as add_scheduled_development
from modeling.develop import develop
from utils.interface import save_to_file, open_dbf
from utils.aa_luz_export import export_luz_data, CROSSWALK_FILEPATH
from utils.config import parameters
from utils.data_prep import create_version_4point1


def run(mgra_dataframe, planned_sites):
    output_dir = parameters['output_directory']
    simulation_years = parameters['simulation_years']
    simulation_begin = parameters['simulation_begin']

    for i in range(simulation_years):
        forecast_year = simulation_begin + i + 1
        if planned_sites is not None:
            print('adding scheduled development:')
            add_scheduled_development(
                mgra_dataframe, planned_sites,
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
    if parameters is not None:
        # prep input
        if not os.path.exists('data/SRF_Input_Base_V4.1.csv'):
            create_version_4point1()
        # load dataframe
        mgra_dataframe = pandas.read_csv(parameters['input_filename'])
        # load scheduled development if a file is available
        scheduled_development_filepath = parameters['sites_filename']
        if os.path.isfile(scheduled_development_filepath):
            planned_sites = open_dbf(scheduled_development_filepath)
        else:
            print('no scheduled development file found (\"{}\"), skipping'
                  .format(scheduled_development_filepath))
            planned_sites = None
        # start simulation
        run(mgra_dataframe, planned_sites)
