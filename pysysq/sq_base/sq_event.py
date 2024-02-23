from typing import Callable


class SQEvent:
    def __init__(self, _name: str, action: Callable, owner):
        self.name = _name
        self.owner = owner
        self.sim_queuing_timestamp = 0
        self.sim_processing_timestamp = 0
        self.host_timestamp = None
        self.scheduled_tick = 0
        self.action = action
