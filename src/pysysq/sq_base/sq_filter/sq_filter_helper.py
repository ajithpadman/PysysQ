from ..sq_packet import SQPacket
from abc import ABC, abstractmethod


class SQFilterHelper(ABC):

    def __init__(self):
        self.owner = None

    def set_owner(self, owner):
        self.owner = owner

    @abstractmethod
    def filter(self, pkt: SQPacket) -> bool:
        pass
