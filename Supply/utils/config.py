import logging

from utils.interface import get_args, load_parameters, empty_folder, \
    save_to_file


def configure():
    args = get_args()
    try:
        if args.test:
            # only meet_demand.py should use a test argument
            parameters = load_parameters('test_parameters.yaml')
        else:
            parameters = load_parameters('parameters.yaml')
    except(FileNotFoundError):
        parameters = None

    if parameters is not None:
        # prep output directory
        output_dir = parameters['output_directory']
        empty_folder(output_dir)
        save_to_file(parameters, output_dir,
                     'parameters_used.yaml', as_yaml=True)
        # configure logging level
        if parameters['debug']:
            logging.basicConfig(level=logging.DEBUG)
    else:
        print('could not load parameters, exiting')
    return parameters


parameters = configure()
