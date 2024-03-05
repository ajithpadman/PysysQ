from abc import ABC, abstractmethod
from typing import Union

from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_packet import SQPacket


class SQQueue(SQObject):


    @abstractmethod
    def pop(self) -> Union[SQPacket,None]:
        pass
