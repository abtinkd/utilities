from __future__ import print_function
import os
import time
from subprocess import call

SUCCESS_LOG = 'SUCCESS_{}.log'.format(time.strftime('%m%d_%H%M'))


def write_success_log(message, prefix=''):
    with open(prefix+SUCCESS_LOG, 'a') as fp:
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
    write_success_log('{}  -->  {}\n'.format(path + '/' + file_name, path + '/' + newfilename), 'append_dir_')


def run_bash_commands(command, file_path):
    file_name, dir_name, cur_path = break_file_path(file_path)

    cmd_inplace = False
    extension = None
    if '@' in command:
        if command[-1] == '@':
            command += 'echo <>'
        flags, command = command.split('@', 1)
        flags = flags.split()
        for flg in flags:
            if flg == 'I':
                cmd_inplace = True
            elif 'f=' in flg:
                extension = '.' + flg[2:].replace('.', '')
    if extension and extension not in file_name:
        return
    command = command.replace('<>', file_name)

    cwd = os.getcwd()

    try:
        os.chdir(cur_path)
        call(command.split())
        if cmd_inplace:
            command = input(': ')
            while command.strip() != 'n':
                call(command.split())
                command = input(': ')

    except Exception as e:
        print('ERROR')
        raise e
    finally:
        os.chdir(cwd)

