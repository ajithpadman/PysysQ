import logging

from pysysq.logging_ctx import SIMLoggingCtx
from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_event_manager import SQEventManager
from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_object import SQObject


class SQServer(SQObject):

    def process(self, evt: SQEvent):
        super().process(evt)
        if self.tick % self.service_clk_ticks != 0 or self.tick == 0:
            self.tick += 1
            self.logger.debug(f'Increment Tick {self.tick}')
        else:
            self.finish_indication()
            if evt.owner is not self:
                evt.owner.disconnect(self)

    def __init__(self, name: str, params, event_mgr: SQEventManager, event_q: int = 1):
        super().__init__(name, params, event_mgr,event_q)
        self.service_clk_ticks = getattr(params, "service_clk_ticks")
        self.logger = SQLogger(self.__class__.__name__,self.name)

