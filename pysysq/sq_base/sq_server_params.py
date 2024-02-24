
from pysysq.sq_base.sq_object_params import SQObjectParams
from dataclasses import dataclass


@dataclass
class SQServerParams(SQObjectParams):
    service_clk_ticks: int

