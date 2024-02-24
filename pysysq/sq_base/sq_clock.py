import time
import logging
from typing import Type, Callable

from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_event_manager import SQEventManager
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_time_base import SQTimeBase


class SQClock(SQObject):

    def __init__(self, params, event_mgr: SQEventManager):
        super().__init__(params, event_mgr)

        self.no_steps = getattr(params, "clk_time_steps")
        self.connect(self)

    def get_current_tick(self):
        return self.tick

    def update_tick(self, ticks: int):
        self.tick += ticks
        logging.info(f'[{self.params.name}:process]: Current Tick {self.tick}')

    def init(self):
        logging.info(f'[{self.params.name}:init]: Current Tick {self.tick}')

    def deinit(self):
        logging.info(f'[{self.params.name}:deinit]: Current Tick {self.tick}')

    def start(self):
        self.tick = 0
        logging.info(f'[{self.params.name}:start]: Current Tick {self.tick}')
        self.schedule()

    def process(self):
        self.tick += 1
        logging.info(f'[{self.params.name}:process]: Current Tick {self.tick}')
        self.schedule(when=self.no_steps)

