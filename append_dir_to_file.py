from core import tools
from core import traverse as td
import sys


if __name__ == '__main__':
    td.apply(sys.argv[1], tools.append_parent_dirname)
