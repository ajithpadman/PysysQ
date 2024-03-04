import logging

from pysysq.logging_ctx import SIMLoggingCtx
from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_object import SQObject


class SQQueue(SQObject):
    def __init__(self, name: str, params, event_mgr):
        super().__init__(name, params, event_mgr)
        self.queue = []
        self.capacity = params.capacity
        self.logger = SQLogger(self.__class__.__name__,self.name)
        self.dropped_pkt_count = 0
        self.register_property('dropped_pkt_count')

    def process(self, evt: SQEvent):
        super().process(evt)
        if len(self.queue) < self.capacity:
            self.queue.append(evt.data)
            self.logger.info(f'{self.name} Queued {evt.data}')
        else:
            self.logger.warning(f'{self.name} Queue Full , Dropping Packet {evt.data}')
            self.dropped_pkt_count += 1

    def pop(self):
        if len(self.queue) == 0:
            return None
        return self.queue.pop(0)
