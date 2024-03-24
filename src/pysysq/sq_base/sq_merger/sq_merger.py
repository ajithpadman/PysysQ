from typing import List
from ..sq_object import SQObject
from ..sq_queue import SQQueue
from ..sq_logger import SQLogger
from ..sq_clock import SQClock

class SQMerger(SQObject):
    def __init__(self, name: str, event_mgr, input_qs: List[SQQueue], output_q: SQQueue, clk: SQClock, **kwargs):
        super().__init__(name, event_mgr, **kwargs)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.rx_qs = input_qs
        self.tx_q = output_q
        self.clk = clk
        if self.clk is not None:
            self.clk.control_flow(self)
        if len(self.rx_qs) <= 1:
            raise ValueError('At least two rx_queue should be provided')
        if self.tx_q is None:
            raise ValueError('tx_queue should be provided')
        for p in self.rx_qs:
            if not isinstance(p, SQQueue):
                raise ValueError(f'rx_q should be a SQQueue object , got {type(p)} instead.')
        if not isinstance(self.tx_q, SQQueue):
            raise ValueError(f'tx_q should be a SQQueue object , got {type(self.tx_q)} instead.')

    def process_packet(self, evt):
        super().process_packet(evt)
        if evt.owner is self.clk:
            for q in self.rx_qs:
                if q.peek() is not None:
                    self.tx_q.push(q.pop())
            self.finish_indication()
        else:
            if evt.name != f'{self.name}_start':
                self.logger.error(f'Ignoring other Events other than Clock Events {evt}')
