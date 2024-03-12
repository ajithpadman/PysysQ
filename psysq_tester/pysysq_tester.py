import logging

from pysysq import *

logger = logging.getLogger("Tester")

if __name__ == '__main__':
    generate(json_file='input.json')
