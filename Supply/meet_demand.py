from modeling.develop import develop
from utils.interface import save_to_file, open_mgra_io_file, parameters


def run(mgra_dataframe):
    output_dir = parameters['output_directory']
    simulation_begin = parameters['simulation_begin']

    forecast_year = simulation_begin + 1
    print('simulating year {}'.format(forecast_year))

    # develop enough land to meet demand for this year.
    mgra_dataframe = develop(mgra_dataframe)
    if mgra_dataframe is None:
        print('program terminated early')
        return

    # save output file
    save_to_file(mgra_dataframe, output_dir,
                 'forecasted_year_{}.csv'.format(forecast_year))

    return


if __name__ == "__main__":
    if parameters is not None:
        run(open_mgra_io_file(from_database=parameters['use_database']))
