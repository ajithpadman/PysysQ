from typing import List, Union

from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_packet import SQPacket
from pysysq.sq_base.sq_queue.sq_queue import SQQueue


class SQSingleQueue(SQQueue):
    def push(self, pkt: SQPacket):
        super().push(pkt)
        if len(self.queue) < self.capacity:
            self.queue.append(pkt)
            self.logger.info(f'Packet Queued {pkt}')
            self.queued_pkt_count += 1
            self.finish_indication()
        else:
            self.logger.warning(f' Queue Full , Dropping Packet {pkt}')
            self.dropped_pkt_count += 1

    def peek(self):
        if len(self.queue) == 0:
            return None
        return self.queue[0]

    def is_empty(self) -> bool:
        return len(self.queue) == 0

    def __init__(self, name: str, event_mgr, **kwargs):
        super().__init__(name, event_mgr, **kwargs)
        self.queue: List[SQPacket] = []
        self.capacity = kwargs.get('capacity', 10)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.dropped_pkt_count = 0
        self.queued_pkt_count = 0
        self.register_property('dropped_pkt_count')
        self.register_property('queued_pkt_count')

    def pop(self, **kwargs) -> Union[SQPacket, None]:
        super().pop()
        if len(self.queue) == 0:
            return None
        return self.queue.pop(0)

    def process(self, evt: SQEvent):
        super().process(evt)
        if evt.owner is not self:
            self.push(evt.data)
        else:
            if evt.name != f'{self.name}_start':
                self.logger.error(f'Ignoring Self Event {evt}')
