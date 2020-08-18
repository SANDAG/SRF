import psycopg2
import pandas
from tqdm import tqdm

from modeling.develop import develop
from utils.interface import \
    load_parameters, save_to_file
from utils.config import parameters


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


def connect_to_db():
    # Set up database connection parameters
    connection_info = load_parameters(
        parameters['database_info_filename'])
    print(connection_info)
    return psycopg2.connect(
        database=connection_info['aa_database'],
        host=connection_info['aa_host'],
        port=connection_info['aa_port'],
        user=connection_info['aa_user'],
        password=connection_info['aa_password'])


if __name__ == "__main__":
    # load parameters
    if parameters is not None:
        # load dataframe
        mgra_dataframe = pandas.read_csv(parameters['input_filename'])
        # load from database
        # conn = connect_to_db()
        # print(conn)
        # mysql = 'select * from {}.\"{}\"'.format(
        #     config.parameters['srf_schema'], config.parameters[
        # 'srf_inputtbl'])
        # mgra_dataframe = pandas.read_sql(mysql, conn)
        # conn.close()

        run(mgra_dataframe)
