import pandas
from tqdm import tqdm

from utils.interface import \
    load_parameters, empty_folder, save_to_file, get_args
import utils.config as config

from modeling.develop import develop
# from modeling.filters import filter_all


def run(mgra_dataframe):
    output_dir = config.parameters['output_directory']
    simulation_years = config.parameters['simulation_years']
    simulation_begin = config.parameters['simulation_begin']
    # debug = config.parameters['debug']

    # the number of tqdm progress bar steps per simulation year
    checkpoints = 7
    progress = tqdm(desc='progress', total=simulation_years *
                    checkpoints, position=0)
    for i in range(simulation_years):
        forecast_year = simulation_begin + i + 1
        progress.set_description('starting year {}'.format(i+1))

        # drop unusable mgras
        # filtered = filter_all(mgra_dataframe)
        # # print("MGRA's under consideration: {}/{}".format(len(filtered),
        # #                                         len(mgra_dataframe)))
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
    args = get_args()
    if args.test:
        config.parameters = load_parameters('test_parameters.yaml')
    else:
        config.parameters = load_parameters('parameters.yaml')

    if config.parameters is not None:
        output_dir = config.parameters['output_directory']
        empty_folder(output_dir)
        save_to_file(config.parameters, output_dir, 'parameters.txt')

        mgra_dataframe = pandas.read_csv(config.parameters['input_filename'])

        run(mgra_dataframe)
    else:
        print('could not load parameters, exiting')
