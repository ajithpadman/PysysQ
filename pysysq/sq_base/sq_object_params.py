from dataclasses import dataclass, field
from typing import List

from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_params import SQParams


@dataclass
class SQObjectParams(SQParams):
    children: List["SQObject"] = field(default_factory=list)
