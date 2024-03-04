from pysysq.sq_base.sq_clock import SQClock
from pysysq.sq_base.sq_object_params import SQObjectParams
from pysysq.sq_base.sq_packet import SQPacket
from dataclasses import dataclass, field
import numpy as np

from pysysq.sq_base.sq_queue import SQQueue


@dataclass
class SQPktProcessorParams(SQObjectParams):
    clk: SQClock = None
    queue: SQQueue = None
    pkt_class: [] = field(default_factory=list)

    def calculate_service_ticks(self, pkt: SQPacket):
        if pkt.size <= 100:
            return np.random.randint(1, 3)
        elif pkt.size <= 200:
            return np.random.randint(2, 8)
        elif pkt.size <= 300:
            return np.random.randint(5, 10)
        else:
            return np.random.randint(10, 15)

    def is_pkt_for_me(self, pkt: SQPacket):
        return pkt.class_name in self.pkt_class
