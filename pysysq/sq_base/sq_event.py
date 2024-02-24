from typing import Callable, List


class SQEvent:
    def __init__(self, _name: str, owner):
        self.name = _name
        self.owner = owner
        self.sim_queuing_timestamp = 0
        self.sim_processing_timestamp = 0
        self.host_timestamp = None
        self.scheduled_tick = 0
        self.actions = []

    def add_handler(self, action: Callable):
        self.actions.append(action)
