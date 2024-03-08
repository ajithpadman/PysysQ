from dataclasses import dataclass


@dataclass
class SQPacket:
    id: int = 0
    size: int = 0
    priority: int = 0
    class_name: str = ""
    generation_time: int = 0
