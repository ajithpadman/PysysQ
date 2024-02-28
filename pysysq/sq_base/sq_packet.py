from dataclasses import dataclass


@dataclass
class SQPacket:
    def __init__(self):
        pkt_id: int
        pkt_size: int
        pkt_class: int
        pkt_priority: int
