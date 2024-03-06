import copy
from typing import List, Union

from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_packet import SQPacket
from pysysq.sq_base.sq_queue.sq_pkt_priority_q_selector import SQPktPriorityQSelector

from pysysq.sq_base.sq_queue.sq_queue import SQQueue
from pysysq.sq_base.sq_queue.sq_queue_selection import QueueSelection
from pysysq.sq_base.sq_queue import SQSingleQueue
from pysysq.sq_base.sq_queue.sq_rr_scheduler import SQRRScheduler


class SQMultiQueue(SQQueue):

    def pop(self):
        pkt = self.scheduler.get(self).pop()
        return pkt

    def __init__(self, name: str, event_mgr, **kwargs):
        super().__init__(name, event_mgr, **kwargs)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.no_of_queues = kwargs.get('no_of_queues', 2)

        self.queues: List[SQQueue] = kwargs.get('queues',
                                                [SQSingleQueue(name=f'{name}_Queue_{i}', event_mgr=event_mgr, **kwargs)
                                                 for i in
                                                 range(self.no_of_queues)])
        self.q_selector = kwargs.get('q_selector', SQPktPriorityQSelector(queues=self.queues))
        self.scheduler = kwargs.get('scheduler', SQRRScheduler(queues=self.queues))
        self.no_of_queues = len(self.queues)
        self.current_queue = self.queues[0]

    def process(self, evt):
        super().process(evt)
        if evt.owner is not self:
            self.current_queue = self.q_selector.get(evt.data)
            self.current_queue.process(copy.copy(evt))
            self.finish_indication()
        else:
            if evt.name != f'{self.name}_start':
                self.logger.error(f'Ignoring Self Event {evt}')

    def get_queue(self, index):
        return self.queues[index]
