import os
import shutil
import yaml
import argparse


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


def empty_folder(folder):
    # trying to avoid emptying an important folder by accident
    if folder != os.getcwd() and \
            (folder.__contains__('out') or folder.__contains__('temp')):
        # if the folder name is somewhat reasonable, go ahead and empty it.
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
                return 1
        return 0
    else:
        print('Did not empty folder \"{}\", check parameter naming'
              .format(folder))
        return 2


def save_to_file(printable, output_directory, filename):
    filepath = os.path.join(output_directory, filename)
    # use pandas to_csv function if available
    if hasattr(printable, 'to_csv'):
        printable.to_csv(filepath, index=False)
    else:
        print(printable, file=open(filepath, 'w'), end='')
