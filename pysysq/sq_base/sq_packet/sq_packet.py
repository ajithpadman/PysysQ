from dataclasses import dataclass


@dataclass
class SQPacket:
    size: int = 0
    priority: int = 0
    class_name: str = ""
    arrival_time: int = 0
