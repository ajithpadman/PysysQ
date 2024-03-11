
from pysysq.sq_base.sq_packet import SQPacket
from abc import ABC, abstractmethod


class SQFilterHelper(ABC):
    @abstractmethod
    def filter(self, pkt: SQPacket) -> bool:
        pass
