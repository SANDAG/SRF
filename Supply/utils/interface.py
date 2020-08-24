from __future__ import print_function
import os
import shutil
import yaml
import argparse
import matplotlib.pyplot as plt
from simpledbf import Dbf5


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='test',
                        default=False, action='store_true')
    return parser.parse_args()


def load_parameters(param_filename):
    with open(param_filename, 'r') as stream:
        try:
            parameters = yaml.safe_load(stream)
            return parameters
        except yaml.YAMLError as error:
            print(error)
    return None


def create_folder_if_needed(folder):
    """
        returns true if folder needed to be created
    """
    if os.path.isdir(folder):
        return False
    else:
        os.mkdir(folder)
        return True


def empty_folder(folder):
    # trying to avoid emptying an important folder by accident
    # if the folder name is somewhat reasonable, go ahead and empty it.
    if not create_folder_if_needed(folder):
        if folder != os.getcwd() and \
                (folder.__contains__('out') or folder.__contains__('temp')):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' %
                          (file_path, e))
                    return 1
            return 0
        else:
            print('Did not empty folder \"{}\", check parameter naming'
                  .format(folder))
            return 2


def save_to_file(printable, output_directory, filename, output_status=True):
    if(output_status):
        print('saving {} to {} folder'.format(filename, output_directory))
    create_folder_if_needed(output_directory)
    filepath = os.path.join(output_directory, filename)
    # use pandas to_csv function if available
    if hasattr(printable, 'to_csv'):
        printable.to_csv(filepath, index=False)
    else:
        print(printable, file=open(filepath, 'w'), end='')
    if(output_status):
        print('saved')


def plot_data(data, output_dir='data/output', image_name='plot.png'):
    plt.plot(data, 'ro')
    plt.savefig(os.path.join(output_dir, image_name))
    plt.close()


def open_dbf(filepath):
    dbf = Dbf5(filepath)
    return dbf.to_dataframe()
