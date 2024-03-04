from dataclasses import dataclass


@dataclass
class SQPacket:
    size: int
    priority: int
    class_name: str
    arrival_time: int
