import logging.config
from os import path
from os.path import dirname, abspath
logging.config.fileConfig(path.join((dirname(abspath(__file__))), 'logging.conf'))