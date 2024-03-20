
from pysysq import *


if __name__ == '__main__':
    sim = SQSimSetupGen(json_file="input.json")
    sim.generate(output_folder="output")
