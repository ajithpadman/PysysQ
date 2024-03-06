from abc import ABC, abstractmethod
from typing import List, Union

from pysysq.sq_base.sq_packet import SQPacket
from pysysq.sq_base.sq_queue import SQQueue


class SQQueueSelector(ABC):
    def __init__(self, queues: List[SQQueue]):
        self.queue_list = queues

    @abstractmethod
    def get(self, pkt: SQPacket) -> Union[SQQueue, None]:
        pass
