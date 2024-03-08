from abc import ABC, abstractmethod
from typing import List

from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_queue import SQQueue


class SQQueueSelector(ABC):
    def __init__(self, queues: List[SQQueue]):
        self.q_list = queues

    @abstractmethod
    def get_rx_q(self, pkt, requester: SQObject) -> SQQueue:
        pass

    @abstractmethod
    def get_tx_q(self, requester: SQObject) -> SQQueue:
        pass

