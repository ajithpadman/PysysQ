import copy
from typing import List
from ..sq_object import SQObject
from ..sq_queue import SQQueue
from ..sq_logger import SQLogger
from ..sq_clock import SQClock


class SQSplitter(SQObject):
    def __init__(self, name: str, event_mgr,input_q:SQQueue, output_qs: List[SQQueue],clk:SQClock, **kwargs):
        super().__init__(name, event_mgr, **kwargs)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.tx_qs = output_qs
        self.input_q = input_q
        self.clk = clk
        if self.clk is not None:
            self.clk.control_flow(self)
        for p in self.tx_qs:
            if not isinstance(p, SQQueue):
                raise ValueError(f'rx_q should be a SQQueue object , got {type(p)} instead.')

    def process_packet(self, evt):
        super().process_packet(evt)
        if evt.owner is self.clk:
            pkt = self.input_q.pop()
            for q in self.tx_qs:
                if pkt is not None:
                    self.logger.info(f'Pushing Packet {evt.data} to Queue {q.name}')
                    q.push(copy.copy(pkt))
            self.finish_indication()
        else:
            if evt.name != f'{self.name}_start':
                self.logger.error(f'Ignoring Events other than Clock Event {evt}')
