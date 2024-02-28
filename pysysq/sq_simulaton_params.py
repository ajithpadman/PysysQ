from typing import List

from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_object_params import SQObjectParams


from dataclasses import dataclass


@dataclass
class SQSimulationParams(SQObjectParams):
    max_sim_time: int = 1000
    time_step: float = 0.10
