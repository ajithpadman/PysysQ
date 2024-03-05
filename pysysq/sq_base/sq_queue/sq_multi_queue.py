import copy
from typing import List, Union

from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_packet import SQPacket
from pysysq.sq_base.sq_queue.sq_default_dyn_q_selector import SQDefaultDynQSelector
from pysysq.sq_base.sq_queue.sq_queue import SQQueue
from pysysq.sq_base.sq_queue.sq_queue_selection import QueueSelection
from pysysq.sq_base.sq_queue import SQSingleQueue


class SQMultiQueue(SQQueue):

    def pop(self) -> Union[SQPacket, None]:
        pkt = self.queues[self.current_queue].pop()
        return pkt

    def __init__(self, name: str, event_mgr, **kwargs):
        super().__init__(name, event_mgr, **kwargs)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.no_of_queues = kwargs.get('no_of_queues', 2)
        self.q_selection = kwargs.get('queue_selection_policy', QueueSelection.ROUND_ROBIN)
        self.dynamic_q_selector = kwargs.get('dynamic_queue_selector', SQDefaultDynQSelector())
        self.queues = kwargs.get('queues',
                                 [SQSingleQueue(name=f'{name}_Queue_{i}', event_mgr=event_mgr, **kwargs) for i in
                                  range(self.no_of_queues)])
        self.current_queue = 0

    def process(self, evt):
        super().process(evt)
        if evt.owner is not self:
            if self.q_selection == QueueSelection.DYNAMIC:
                self.current_queue = self.dynamic_q_selector.get(evt.data)
                if self.current_queue < 0 or self.current_queue >= self.no_of_queues:
                    raise ValueError(f'Invalid Queue Selection {self.current_queue}. '
                                     f' Please check the Dynamic Queue Selector Configuration')
                self.logger.info(f'Selected Queue through dynamic port selection  {self.current_queue}')
                self.queues[self.current_queue].process(copy.copy(evt))
                self.finish_indication()
            elif self.q_selection == QueueSelection.ROUND_ROBIN:
                self.current_queue = (self.current_queue + 1) % len(self.queues)
                self.queues[self.current_queue].process(copy.copy(evt))
                self.logger.info(f' Selected Queue through Round Robin port selection  {self.current_queue}')
                self.finish_indication()
            else:
                self.logger.error(f'Unknown Queue Selection Policy {self.q_selection}')
        else:
            if evt.name != f'{self.name}_start':
                self.logger.error(f'Ignoring Self Event {evt}')

    def get_queue(self, index):
        return self.queues[index]
