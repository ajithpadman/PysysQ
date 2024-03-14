from abc import ABC, abstractmethod
from typing import Union

from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_packet import SQPacket


class SQQueue(SQObject):

    def pop(self, **kwargs):
        self.collect_statistics()

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def peek(self):
        pass

    def push(self, pkt: SQPacket):
        pkt.path.append(self.name)
        self.collect_statistics()
