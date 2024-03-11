import copy
from typing import List

from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_queue import SQQueue


class SQSplitter(SQObject):
    def __init__(self, name: str, event_mgr, tx_qs: List[SQQueue], **kwargs):
        super().__init__(name, event_mgr, **kwargs)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.tx_qs = tx_qs
        for p in self.tx_qs:
            if not isinstance(p, SQQueue):
                raise ValueError(f'rx_q should be a SQQueue object , got {type(p)} instead.')

    def process_packet(self, evt):
        super().process_packet(evt)
        if evt.owner is not self:
            for q in self.tx_qs:
                self.logger.info(f'Pushing Packet {evt.data} to Queue {q.name}')
                q.push(copy.copy(evt.data))
            self.finish_indication(evt.data)
        else:
            if evt.name != f'{self.name}_start':
                self.logger.error(f'Ignoring Self Event {evt}')
