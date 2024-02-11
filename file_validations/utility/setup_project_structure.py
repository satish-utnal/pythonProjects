"""

One-time run to generate directory structure for landing/processing files.

"""

import os
import datetime as dt
import configparser


def create_src_dir(data_directory, root_dir):
    """
    create src_dir function which receives two parameters and creates the folders structure
    :param data_directory:  receives folder names like incoming_files, success files
    :param root_dir: under which path the data directory need to be created in this case inside data directory
    :return: No return from this function as it just creates required directory
    """
    child_dir = dt.datetime.now().strftime('%Y%m%d')
    path = '../' + root_dir + '/' + data_directory
    try:
        if not os.path.isdir(path):
            os.mkdir(path)
            print(f'{path} - directory created')
        else:
            print(f'{path} directory already present and will not be created')
        if not os.path.isdir(path + '/' + child_dir):
            os.mkdir(path + '/' + child_dir)
            print(f'{path}/{child_dir} - Directory created')
        else:
            print(f'{path}/{child_dir} - directory already present and will not be created')
    except Exception as e:
        print(f'Failed to create directory with error - {e}')


def create_main_dir(main_dir):
    """

    :param main_dir: receives main projects directory names to create like data, log
    :return: No return as it just creates directory structure
    """
    print(main_dir)
    try:
        if not os.path.isdir('../' + main_dir):
            os.mkdir('../' + main_dir)
            print(f'../{main_dir} - directory created')
        else:
            print(f'../{main_dir} directory already present and will not be created')
    except Exception as e:
        print(f'Failed to create directory with error - {e}')


if __name__ == "__main__":
    """
    script execution starts from this main function
    """
    config = configparser.ConfigParser()
    config.read('../config/config.ini')
    paths = config['Paths']
    folders_to_create = paths['folders_to_create']
    folders_to_create = folders_to_create.split(',')
    data_folder = paths['data_folder']
    log_folder = paths['log_folder']
    create_main_dir(str(data_folder))
    create_main_dir(log_folder)
    for directory in folders_to_create:
        create_src_dir(directory, data_folder)
