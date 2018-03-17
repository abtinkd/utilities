import argparse
import functools
from core import tools
from core import traverse


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Traverse directory and run bash commands.')
    parser.add_argument('--cmd', default='I @ echo <>',
                        help='''Execute this bash command on each file. 
                        (use @ to separate pre-process flags; Ex. \'I f=.txt @ wc -l <>\') 
                        [I] enables in-place run command mode;
                        [f=.*] executes command on the files with the extension defined.''')
    parser.add_argument('--src', default='', help='Input directory to be processed.')

    args = parser.parse_args()
    run_this_command = functools.partial(tools.run_bash_commands, args.cmd)
    traverse.apply(args.src, run_this_command)
