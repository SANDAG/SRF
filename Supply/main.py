import os
import logging

from scheduled_development import run as add_scheduled_development
from modeling.develop import develop
from utils.interface import save_to_file, empty_folder, open_mgra_io_file, \
    open_sites_file
from utils.parameter_access import parameters
from utils.aa_floorspace_update import update_floorspace



def exception_handler(exception_type, exception, traceback):
    print('%s: %s' % (exception_type.__name__, exception))


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
    save_to_file(mgra_dataframe, output_dir,
                 'forecasted_year_{}.csv'.format(forecast_year))
    # create aa export if crosswalk is available
    print('updating AA floorspace file ...')
    update_floorspace(mgra_dataframe, forecast_year)
    return


if __name__ == "__main__":
    import sys
    sys.tracebacklimit = 0
    sys.excepthook = exception_handler

    if parameters is not None:
        # prep output directory
        output_dir = parameters['output_directory']
        empty_folder(output_dir)
        save_to_file(parameters, output_dir,
                     'parameters_used.yaml', as_yaml=True, output_status=False)
        # configure logging level
        if parameters['debug']:
            if parameters['to_file']:
                sys.stderr = open(
                    os.path.join(output_dir, 'debug_output'),
                    mode='x'
                )
            logging.basicConfig(level=logging.DEBUG)

        # load dataframe(s)
        use_database = parameters['use_database']
        mgra_dataframe = open_mgra_io_file(
            from_database=use_database, filename=parameters['input_filename'])
        planned_sites = open_sites_file(from_database=True)

        # start simulation
        run(mgra_dataframe, planned_sites)
