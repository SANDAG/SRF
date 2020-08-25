
from scheduled_development import run as add_scheduled_development
from modeling.develop import develop
from utils.interface import save_to_file, open_mgra_io_file, open_sites_file, \
    parameters
from utils.aa_luz_export import export_luz_data


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
        export_luz_data(mgra_dataframe)
        print('Done')
    return


if __name__ == "__main__":
    if parameters is not None:
        # load dataframe(s)
        mgra_dataframe = open_mgra_io_file(from_database=True)
        planned_sites = open_sites_file(from_database=True)
        # start simulation
        run(mgra_dataframe, planned_sites)
