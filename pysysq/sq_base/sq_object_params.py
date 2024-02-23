from dataclasses import dataclass

from pysysq.sq_base.sq_params import SQParams


@dataclass
class SQObjectParams(SQParams):
    evt_q: int


