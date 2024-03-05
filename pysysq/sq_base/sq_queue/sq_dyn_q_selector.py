from abc import ABC, abstractmethod

from pysysq.sq_base.sq_packet import SQPacket


class SQDynQSelector(ABC):
    @abstractmethod
    def get(self, pkt:SQPacket):
        pass
