import logging.config
from os import path

from os.path import dirname, abspath
from src.pysysq.sq_base.sq_sim_setup_generator import SQSimSetupGen

logging.config.fileConfig(path.join((dirname(abspath(__file__))), 'logging.conf'))
