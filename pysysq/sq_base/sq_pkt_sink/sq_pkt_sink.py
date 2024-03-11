from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_queue import SQSingleQueue


class SQPktSink(SQObject):
    def __init__(self, name: str, event_mgr, **kwargs):
        super().__init__(name, event_mgr, **kwargs)
        self.logger = SQLogger(self.__class__.__name__, self.name)

    def process_packet(self, evt: SQEvent):
        super().process_packet(evt)
        curr_pkt = evt.data
        if curr_pkt is not None:
            self.tick += 1
            self.logger.info(f' Terminated the Packet {curr_pkt}')