from tqdm import tqdm

from modeling.develop import develop
from utils.interface import save_to_file, open_mgra_io_file, parameters


def run(mgra_dataframe):
    output_dir = parameters['output_directory']
    simulation_years = parameters['simulation_years']
    simulation_begin = parameters['simulation_begin']

    for i in range(simulation_years):
        forecast_year = simulation_begin + i + 1
        print('simulating year {}'.format(forecast_year))

        # develop enough land to meet demand for this year.
        mgra_dataframe = develop(mgra_dataframe)
        if mgra_dataframe is None:
            print('program terminated, {} years were completed'.format(i))
            return
        progress = tqdm(total=1)
        progress.set_description(
            'saving year{}_{}.csv'.format(i+1, forecast_year))
        save_to_file(mgra_dataframe, output_dir, 'year{}_{}.csv'.format(
            i + 1, forecast_year))
        progress.update()
        progress.close()
    return


if __name__ == "__main__":
    if parameters is not None:
        run(open_mgra_io_file())
