from enum import Enum


class PortSelection(Enum):
    DYNAMIC = 1
    ROUND_ROBIN = 2
    BROADCAST = 3
