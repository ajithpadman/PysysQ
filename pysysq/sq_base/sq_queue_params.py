
from pysysq.sq_base.sq_object_params import SQObjectParams
from dataclasses import dataclass


@dataclass
class SQQueueParams(SQObjectParams):
    capacity: int = 10

