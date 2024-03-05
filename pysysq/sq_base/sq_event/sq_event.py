from typing import Callable, Union

from pysysq.sq_base.sq_packet import SQPacket
from pysysq.sq_base.sq_packet.sq_packet_info import SQPacketInfo


class SQEvent:
    def __init__(self, _name: str, owner):
        self.name = _name
        self.owner = owner
        self.sim_queuing_timestamp = 0
        self.sim_processing_timestamp = 0
        self.host_timestamp = None
        self.scheduled_tick = 0
        self.data: Union[SQPacket, None] = None
        self.actions = []

    def add_handler(self, action: Callable):
        if action not in self.actions:
            self.actions.append(action)

    def remove_handler(self, action: Callable):
        self.actions.remove(action)

    def __repr__(self):
        return self.name
