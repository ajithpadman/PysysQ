import copy

from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_queue import SQSingleQueue


class SQSplitter(SQObject):
    def __init__(self, name: str, event_mgr, **kwargs):
        super().__init__(name, event_mgr, **kwargs)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.no_of_qs = kwargs.get('no_of_queues', 2)
        self.rx_qs = kwargs.get('queues', [SQSingleQueue(name=f'{name}_Q_{i}', event_mgr=event_mgr, **kwargs)
                                           for i in
                                           range(self.no_of_qs)])
        self.no_of_qs = len(self.rx_qs)

        for p in self.rx_qs:
            if not isinstance(p, SQSingleQueue):
                raise ValueError(f'rx_q should be a SQQueue object , got {type(p)} instead.')

    def process(self, evt):
        super().process(evt)
        if evt.owner is not self:
            for q in self.rx_qs:
                self.logger.info(f'Pushing Packet {evt.data} to Queue {q.name}')
                q.push(copy.copy(evt.data))
            self.finish_indication(evt.data)
        else:
            if evt.name != f'{self.name}_start':
                self.logger.error(f'Ignoring Self Event {evt}')
