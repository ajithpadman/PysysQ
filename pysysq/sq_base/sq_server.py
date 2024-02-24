import logging
from typing import Type

from pysysq.sq_base.sq_clock import SQClock
from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_event_manager import SQEventManager
from pysysq.sq_base.sq_object import SQObject


class SQServer(SQObject):
    def init(self):
        pass

    def deinit(self):
        pass

    def start(self):
        self.schedule()

    def notify(self, obj: "SQObject"):
        pass

    def process(self):
        if self.tick <= self.service_clk_ticks:
            logging.info(f'{self.params.name}  Process  Tick = {self.tick}')
            self.tick += 1
        else:
            self.schedule()

    def __init__(self, params, event_mgr: SQEventManager):
        super().__init__(params, event_mgr)
        self.service_clk_ticks = getattr(params, "service_clk_ticks")
