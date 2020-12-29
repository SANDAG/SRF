from os import path

from scheduled_development import run as add_scheduled_development
from modeling.develop import develop
from utils.interface import save_to_file, open_mgra_io_file, open_sites_file
from utils.parameter_access import parameters
from utils.aa_luz_export import export_luz_data


def run(mgra_dataframe, planned_sites):
    output_dir = parameters['output_directory']
    forecast_year = parameters['simulation_year']
    
    # add scheduled development if available
    if planned_sites is not None:
        print('adding scheduled development:')
        add_scheduled_development(
            mgra_dataframe, planned_sites, year=forecast_year)
           # year=simulation_begin)
    # finish meeting demand as needed
    print('developing to meet remaining demand:')
    mgra_dataframe = develop(mgra_dataframe)
    if mgra_dataframe is None:
        print('program terminated early')
        return
    # save output file
    save_to_file(mgra_dataframe, path.dirname(output_dir) ,
                 'forecasted_year_{}.csv'.format(forecast_year))
    # create aa export if crosswalk is available
    print('creating AA commodity export file ...')
    export_luz_data(mgra_dataframe)

    return


if __name__ == "__main__":
    if parameters is not None:
        # load dataframe(s)
        use_database = parameters['use_database']
        mgra_dataframe = open_mgra_io_file(from_database=use_database, filename=parameters['input_filename'])
        planned_sites = open_sites_file(from_database=True)

        # start simulation
        run(mgra_dataframe, planned_sites)
