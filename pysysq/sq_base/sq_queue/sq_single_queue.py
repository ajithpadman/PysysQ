from typing import List, Union

from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_packet import SQPacket
from pysysq.sq_base.sq_queue.sq_queue import SQQueue


class SQSingleQueue(SQQueue):
    def __init__(self, name: str, event_mgr, **kwargs):
        super().__init__(name, event_mgr, **kwargs)
        self.queue: List[SQPacket] = []
        self.capacity = kwargs.get('capacity', 10)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.dropped_pkt_count = 0
        self.queued_pkt_count = 0
        self.register_property('dropped_pkt_count')
        self.register_property('queued_pkt_count')

    def process(self, evt: SQEvent):
        super().process(evt)
        if len(self.queue) < self.capacity:
            self.queue.append(evt.data)
            self.logger.info(f'{self.name} Queued {evt.data}')
            self.queued_pkt_count += 1
            self.finish_indication()
        else:
            self.logger.warning(f'{self.name} Queue Full , Dropping Packet {evt.data}')
            self.dropped_pkt_count += 1

    def pop(self) -> Union[SQPacket, None]:
        if len(self.queue) == 0:
            return None
        return self.queue.pop(0)
