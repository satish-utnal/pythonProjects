# @Author Satish Utnal

# This code should execute at the beginning to build up all the appropriate directory structure for the first time.

import os
import datetime as dt


def create_src_dir(path):
    child_dir = dt.datetime.now().strftime('%Y%m%d')
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
        print(f'Failed to create directory incoming_files with error - {e}')


def create_dir():
    create_src_dir("incoming_files")
    create_src_dir("rejected_files")
    create_src_dir("success_files")
