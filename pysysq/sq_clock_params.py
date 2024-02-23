
from dataclasses import dataclass

from pysysq.sq_base.sq_object_params import SQObjectParams


@dataclass
class SQClockParams(SQObjectParams):
    clk_time_steps: int
