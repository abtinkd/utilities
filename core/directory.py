from __future__ import print_function
import os
import sys
import time
from traverse_dir import apply_to


SUCCESS_LOG = 'append_dir_success_{}.log'.format(time.strftime('%m%d_%H%M'))


def write_success_log(message):
    with open(SUCCESS_LOG, 'a') as fp:
        fp.write("{}\n".format(message))


def break_file_path(file_path, separator='/'):
    parts = file_path.rsplit(separator, 2)
    sep_count = file_path.count(separator)
    if sep_count >= 2:
        file_name = parts[2]
        dir_name = parts[1]
        path = parts[0] + separator + dir_name
    else:
        file_name = parts[1]
        dir_name = parts[0]
        path = separator + dir_name
    return file_name, dir_name, path


def append_parent_dirname(file_path):
    file_name, dir_name, path = break_file_path(file_path)
    dir_name = dir_name.replace('.late', '-late')
    newfilename = dir_name + '_' + file_name
    os.rename(path + '/' + file_name, path + '/' + newfilename)
    write_success_log('{}  -->  {}\n'.format(path + '/' + file_name, path + '/' + newfilename))


if __name__ == '__main__':
    apply_to(sys.argv[1], append_parent_dirname, True)
