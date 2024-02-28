import logging
import time

from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_event_manager import SQEventManager
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_time_base import SQTimeBase


class SQSimulator(SQObject):

    def start(self):
        super().start()
        self.process(self.start_evt)

    def process(self, evt: SQEvent):
        # SQTimeBase.update_current_sim_time()
        # self.tick += 1

        while SQTimeBase.get_current_sim_time() < self.max_sim_time:
            self.event_manager.run()
            SQTimeBase.update_current_sim_time()
            self.tick += 1
            self.logger.debug(f'Simulator Tick {self.tick}')
            time.sleep(self.time_step)
        self.event_manager.run()
        self.deinit()

    def __init__(self, name: str, params, event_mgr: SQEventManager):
        super().__init__(name, params, event_mgr)
        SQTimeBase.reset_current_sim_time()
        self.max_sim_time: int = getattr(params, "max_sim_time")
        self.time_step: int = getattr(params, "time_step")
        self.logger = logging.getLogger(self.__class__.__name__)
        self.self_starting = True
