from pysysq.sq_base.sq_object_params import SQObjectParams
from pysysq.sq_base.sq_packet import SQPacket
from abc import abstractmethod


class SQPktGenParams(SQObjectParams):
    @abstractmethod
    def generate(self) -> SQPacket:
        pass
