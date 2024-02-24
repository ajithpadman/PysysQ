import logging
import time

from pysysq.sq_base.sq_event_manager import SQEventManager
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_time_base import SQTimeBase


class SqSimulator(SQObject):

    def init(self):
        logging.info(
            f'Simulator: init')
        for obj in self.sq_objects:
            assert isinstance(obj, SQObject), "all simulation objects must be derived from SQObject"
            obj.init()

    def deinit(self):
        for obj in self.sq_objects:
            obj.deinit()

    def start(self):
        self.init()
        logging.info(
            f'Simulator: start')
        for obj in self.sq_objects:
            obj.start()
        self.process()

    def process(self):
        while SQTimeBase.get_current_sim_time() < self.max_sim_time:
            logging.info(
                f'Simulator: Process Tick')
            SQTimeBase.update_current_sim_time()
            SQTimeBase.update_current_host_time()

            self.event_manager.run()

            time.sleep(self.time_step)
        self.deinit()

    def __init__(self, params, event_mgr: SQEventManager):
        super().__init__(params, event_mgr)
        SQTimeBase.reset_current_sim_time()
        SQTimeBase.reset_current_host_time()
        self.max_sim_time: int = getattr(params, "max_sim_time")
        self.time_step: int = getattr(params, "time_step")
        self.sq_objects = getattr(params, "sq_objects")
        self.init()
