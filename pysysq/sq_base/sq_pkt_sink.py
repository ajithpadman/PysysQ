import logging

from pysysq.logging_ctx import SIMLoggingCtx
from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_object import SQObject


class SqPktSink(SQObject):
    def __init__(self, name: str, params, event_mgr):
        super().__init__(name, params, event_mgr)
        self.logger = SQLogger(self.__class__.__name__,self.name)

    def process(self, evt: SQEvent):
        super().process(evt)
        self.tick += 1
        self.logger.debug(f'{self.name} Sinked {evt.data}')
