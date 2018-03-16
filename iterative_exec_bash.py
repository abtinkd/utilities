import argparse
import functools
from core import tools
from core import traverse


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Traverse directory and run bash commands.')
    parser.add_argument('--bash', default='@ wc -l {}',
                        help='Execute this bash command on each file. (use @ to stay in place)')
    parser.add_argument('--src', default='', help='Input directory to be processed.')
    parser.add_argument('-p', action='store_true', help='Print process')

    args = parser.parse_args()
    run_this_command = functools.partial(tools.run_bash_commands, args.bash)
    traverse.apply(args.src, run_this_command, args.p)
