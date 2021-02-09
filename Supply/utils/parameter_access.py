from utils.interface import load_yaml, empty_folder, save_to_file
import argparse
import logging
import os
import sys


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', "--filename", dest='filename')
    parser.add_argument('-y', "--year", type=int, dest='year')
    parser.add_argument('-t', '--test', dest='test',
                        default=False, action='store_true')
    parser.add_argument('-i', '--include-integration', dest='include',
                        default=False, action='store_true')
    return parser.parse_args()


def configure():
    args = get_args()
    try:
        if args.test:
            # only meet_demand.py should use a test argument
            parameters = load_yaml('test_parameters.yaml')
        else:
            parameters = load_yaml('parameters.yaml')
    except(FileNotFoundError):
        parameters = None

    if parameters is not None:
        parameters['input_filename'] = None
        parameters['include_integration_tests'] = args.include
        if args.filename is not None:
            parameters['input_filename'] = args.filename
            parameters['use_database'] = False
        if args.year is not None:
            parameters['simulation_year'] = args.year

        # TODO: add the control totals here

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

    else:
        print('could not load parameters, exiting')
    return parameters


parameters = configure()
