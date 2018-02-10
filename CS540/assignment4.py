import sys, os, time
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'DirProcess'))
import traverse_dir as td
from subprocess import call

SUCCESS_LOG = 'success_{}.log'.format(time.strftime('%m%d_%H%M'))

def write_success_log(message, file_prefix=''):
    with open(file_prefix+SUCCESS_LOG, 'a') as fp:
                fp.write("{}\n".format(message))

def break_filepath(filepath):
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
    return filename, dirname, path


def attach_username(filepath):       
        filename, dirname, path = break_filepath(filepath)
        dirname = dirname.replace('.late', '-late')
        newfilename = dirname + '_' + filename
        os.rename(path+'/'+filename, path+'/'+newfilename)
        write_success_log('{}  -->  {}\n'.format(path+'/'+filename, path+'/'+newfilename), 'attach_')

def run_code_move(filepath, CSV_PATH = './csv', CPP_PATH = './cpp'):
    filename, dirname, path = break_filepath(filepath)
    newpath = path+'/'+ filename.split('.')[0]    
    os.mkdir(newpath)

    cpp_filepath = CPP_PATH + '/' + filename.split('.')[0] + '.cpp'
    
    call(["mv",filepath, newpath])
    call(['cp', '-r', CSV_PATH+'/.', newpath])
    call(['cp', cpp_filepath, newpath])
    cwd = os.getcwd()
    os.chdir(newpath)
    print 'calling: {}/{}'.format(newpath, filename)
    call(['{}/{}'.format(newpath, filename)])    
    
    join_csv = 'y'
    while join_csv != 'n':        
        call('ls')
        join_csv = raw_input(': ')
        call(['less', join_csv])    
    os.chdir(cwd)

def run_code_inplace(filepath, CSV_PATH = './csv'):
    if filepath[-4:].lower() == '.out':
        filename, dirname, path = break_filepath(filepath)        
        call(['cp', '-r', CSV_PATH+'/.', path])    
        cwd = os.getcwd()
        os.chdir(path)
        print 'calling: {}'.format(filepath)
        
        try:
            call([filepath])            
        except Exception as e:
            print 'ERROR'
            raise e
        else:
            print 'SUCCESS!'
            os.chdir(cwd)            
            write_success_log('{}'.format(filepath), 'run_')
            os.chdir(path)
        finally:
            call(['pwd'])            
            call(['ls'])
            join_csv = '?less join.csv'
            while join_csv != 'n':                
                if join_csv[0] == '?':
                    call(join_csv[1:].split())
                else:
                    call(['less', join_csv])
                join_csv = raw_input(': ')
            os.chdir(cwd) 


def fetch_files(filepath, COPY_DIR = './code'):    
    filename, dirname, path = break_filepath(filepath)
    if filename[-4:].lower() == '.cpp' or filename[-4:].lower() == '.out':
        newpath = COPY_DIR+'/'+ dirname
        if not os.path.exists(newpath):
            os.mkdir(newpath)            
        call(['cp', filepath, newpath])
        write_success_log('{} {} {}'.format(os.path.exists(newpath), filepath, newpath), 'fetch_')

def compile(filepath):
    filename, dirname, path = break_filepath(filepath)        
    if filename[-4:].lower() == '.cpp':
        username = filename.split('_',1)[0]
        x = call(["g++",filepath,"-o", "{}/A_{}_main.out".format(path, username)])
        if x:
            raise ValueError(username)
        write_success_log("g++ {} -o {}/A_{}_main.out".format(filepath, path, username), 'compile_')        


import sys
if __name__ == '__main__':
    root  = './test'
    code = './code'
    if len(sys.argv) > 2:
        root = sys.argv[1]
        code = sys.argv[2]
    elif len(sys.argv) == 2:
        root = sys.argv[1]

    # td.apply_to(root, attach_username)
    # td.apply_to(root, fetch_files)
    # td.apply_to(code, compile)
    td.apply_to(code, run_code_inplace)