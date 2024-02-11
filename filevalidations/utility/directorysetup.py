"""

One-time run to generate directory structure for landing/processing files.

"""

import os
import datetime as dt
import configparser


def create_src_dir(data_folder_path, root_dir):
    child_dir = dt.datetime.now().strftime('%Y%m%d')
    path = '../' + data_folder_path + '/' + root_dir
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


config = configparser.ConfigParser()
config.read('../config/config.ini')
paths = config['Paths']
folders_to_create = paths['folders_to_create']
folders_to_create = folders_to_create.split(',')
print(folders_to_create)
data_folder = paths['data_folder']
for directory in folders_to_create:
    create_src_dir(data_folder, directory)
