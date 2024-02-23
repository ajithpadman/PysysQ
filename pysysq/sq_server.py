from typing import Type

from pysysq.sq_base.sq_event_manager import SQEventManager
from pysysq.sq_base.sq_object import SQObject


class SQServer(SQObject):
    def init(self):
        pass

    def deinit(self):
        pass

    def start(self):
        pass

    def process(self):
        pass

    def __init__(self, params, event_mgr: SQEventManager):
        super().__init__(params, event_mgr)
        self.clk = getattr(params, 'clk')
        assert self.clk is not None, "Clock must be configured for a Server"



