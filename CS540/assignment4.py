import sys, os, time
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'DirProcess'))
import traverse_dir as td
from subprocess import call

SUCCESS_LOG = 'success_{}.log'.format(time.strftime('%m%d_%H%M'))

def attach_username(filepath):
        parts = filepath.rsplit('/', 2)
        if len(parts) > 2:
            filename = parts[2]
            dirname = parts[1]
            path = parts[0] + '/' + dirname
        elif len(parts) == 2:
            filename = parts[1]
            dirname = parts[0]
            path = dirname
        else:
            filename = filepath
            dirname = ''
            path = '.'

        dirname = dirname.replace('.late', '')
        newfilename = dirname + '_' + filename
        os.rename(path+'/'+filename, path+'/'+newfilename)
        with open(SUCCESS_LOG, 'a') as fp:
                fp.write('{}  -->  {}\n'.format(path+'/'+filename, path+'/'+newfilename))

def compile(filepath):
        path = filepath.rsplit('/',1)
        if len(path) > 1:
            filename = path[1]
            path = path[0]
        else:
            filename = path
            path = ''
        username = filename.split('_',1)[0]
        call(["g++",filepath,"-o", "{}/out/{}_main.out".format(path, username)])
        with open(SUCCESS_LOG, 'a') as fp:
                fp.write("g++ {} -o {}/out/{}_main.out\n".format(filepath, path, username))


import sys
if __name__ == '__main__':
    if len(sys.argv) > 1:
        root = sys.argv[1].strip()
    else:
        root  = './test/'
    
    td.apply_to(root, attach_username)