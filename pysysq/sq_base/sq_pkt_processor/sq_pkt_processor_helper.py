from abc import ABC, abstractmethod

from pysysq.sq_base.sq_object import SQObject


class SQPktProcessorHelper(ABC):
    def __init__(self, name: str, owner: SQObject):
        self.owner = owner
        self.name = name

    @abstractmethod
    def get_processing_ticks(self, pkt):
        pass

    @abstractmethod
    def process_packet(self, pkt, tick: int):
        pass
