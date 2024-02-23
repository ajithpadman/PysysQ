from typing import Union, Type

from pysysq.sq_base.sq_packet_params import SQPacketParams


class SQPacket:
    def __init__(self, params: Type[SQPacketParams]):
        self.params = params
