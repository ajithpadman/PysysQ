from dataclasses import dataclass

from pysysq.sq_base.sq_params import SQParams


@dataclass
class SQPacketParams(SQParams):
    pkt_size: int
    pkt_class: str
