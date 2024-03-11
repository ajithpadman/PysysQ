from abc import ABC, abstractmethod
from typing import List

from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_packet import SQPacket
from pysysq.sq_base.sq_queue import SQQueue


class SQMuxDemuxHelper(ABC):
    def __init__(self):
        self.tx_qs = []
        self.rx_qs = []

    def set_tx_queues(self, queues: List[SQQueue]):
        self.tx_qs = queues

    def set_rx_queues(self, queues: List[SQQueue]):
        self.rx_qs = queues

    @abstractmethod
    def get_rx_q(self, requester: SQObject) -> SQQueue:
        pass

    @abstractmethod
    def get_tx_q(self, pkt: SQPacket, requester: SQObject) -> SQQueue:
        pass
