import time
import logging
from typing import Type, Callable

from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_event_manager import SQEventManager
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_time_base import SQTimeBase
from pysysq.sq_clock_params import SQClockParams


class SQClock(SQObject):
    def __init__(self, params, event_mgr: SQEventManager):
        super().__init__(params, event_mgr)
        self.tick: int = 0
        self.no_steps = getattr(params, "clk_time_steps")
        self.clk_evt = SQEvent(_name="default_clk_evt", action=self.default_tick_handler, owner=self)

    def get_current_tick(self):
        return self.tick

    def default_tick_handler(self):
        logging.info(f'[{self.params.name}:DefaultTickHandler]: Current Sim Time{SQTimeBase.get_current_sim_time()} Tick {self.tick}')

    def set_tick_handler(self, action: Callable):
        self.clk_evt.action = action

    def get_next_tick(self):
        return self.tick + 1

    def init(self):
        logging.info(f'[{self.params.name}:Init]: Current Sim Time{SQTimeBase.get_current_sim_time()}')

    def deinit(self):
        logging.info(f'[{self.params.name}:DeInit]: Current Sim Time{SQTimeBase.get_current_sim_time()}')

    def start(self):
        if SQTimeBase.get_current_sim_time() % self.no_steps == 0:
            self.tick += 1
            self.event_manager.schedule(self.clk_evt, SQTimeBase.get_current_sim_time() + self.no_steps)
