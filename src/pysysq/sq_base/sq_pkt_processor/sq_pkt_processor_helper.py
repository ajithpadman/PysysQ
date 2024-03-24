from abc import ABC, abstractmethod
from typing import Union

from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_packet.sq_metadata import SQMetadata


class SQPktProcessorHelper(ABC):
    def __init__(self):
        self.owner = None

    def set_owner(self, owner: SQObject):
        self.owner = owner

    @abstractmethod
    def get_processing_ticks(self, pkt):
        pass

    @abstractmethod
    def process_packet(self, pkt, tick: int) -> Union[SQMetadata, None]:
        pass

    @abstractmethod
    def process_data(self, data: SQMetadata, tick: int):
        pass


