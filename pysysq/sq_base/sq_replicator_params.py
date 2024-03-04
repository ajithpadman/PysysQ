from enum import Enum

from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_object_params import SQObjectParams
from dataclasses import dataclass

from pysysq.sq_base.sq_port_selection import PortSelection


@dataclass
class SQReplicatorParams(SQObjectParams):
    capacity: int = 10
    no_of_ports: int = 2
    port_selection: PortSelection = PortSelection.DYNAMIC

    def get_selected_queue(self, evt: SQEvent):
        return 0
