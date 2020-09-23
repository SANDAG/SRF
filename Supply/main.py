from scheduled_development import run as add_scheduled_development
from modeling.develop import develop
from utils.interface import save_to_file, open_mgra_io_file, open_sites_file, \
    parameters
from utils.aa_luz_export import export_luz_data


def run(mgra_dataframe, planned_sites):
    output_dir = parameters['output_directory']
    simulation_begin = parameters['simulation_begin']

    forecast_year = simulation_begin + 1
    # add scheduled development if available
    if planned_sites is not None:
        print('adding scheduled development:')
        add_scheduled_development(
            mgra_dataframe, planned_sites,
            year=simulation_begin)
    # finish meeting demand as needed
    print('developing to meet remaining demand:')
    mgra_dataframe = develop(mgra_dataframe)
    if mgra_dataframe is None:
        print('program terminated early')
        return
    # save output file
    save_to_file(mgra_dataframe, output_dir,
                 'forecasted_year_{}.csv'.format(forecast_year))
    # create aa export if crosswalk is available
    print('creating AA commodity export file ...')

    export_luz_data(mgra_dataframe)
    return


if __name__ == "__main__":
    if parameters is not None:
        use_database = parameters['use_database']
        # load dataframe(s)
        mgra_dataframe = open_mgra_io_file(from_database=use_database)
        planned_sites = open_sites_file(from_database=use_database)
        # start simulation
        run(mgra_dataframe, planned_sites)
