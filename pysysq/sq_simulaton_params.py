from typing import List

from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_object_params import SQObjectParams
from pysysq.sq_clock_params import SQClockParams

from dataclasses import dataclass


@dataclass
class SQSimulationParams(SQObjectParams):
    max_sim_time: int
    time_step: float
    sq_objects: List[SQObject]
