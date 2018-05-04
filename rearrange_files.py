from __future__ import print_function
from core import traverse
import os
from subprocess import call


def arrange(root_path):
    for file_name, file_path in traverse.access(root_path):
        st_id = file_name.split('_',1)[0]
        if not os.path.exists(file_path + '/' + st_id):
            os.mkdir(file_path + '/' + st_id)

        cur_file = file_path + '/' + file_name
        new_file = file_path + '/' + st_id + '/' + file_name
        call(['mv', cur_file, new_file])


if __name__ == '__main__':
    print("CAUTION! This module changes the structure of the sending directory!")
    print("Give me the absolute path of the WORKING directory: ")
    root_path = input()
    arrange(root_path)
    print('Done!')

