import copy
from typing import List, Union
from ..sq_object import SQObject
from ..sq_queue import SQQueue
from ..sq_clock import SQClock
from ..sq_logger import SQLogger
from .sq_mux_demux_helper import SQMuxDemuxHelper
from ..sq_event import SQEvent


class SQMux(SQObject):
    def __init__(self, name: str,
                 event_mgr,
                 input_qs: List[SQQueue],
                 output_q: Union[SQQueue, None],
                 clk: SQClock,
                 helper: SQMuxDemuxHelper = None,
                 **kwargs):
        super().__init__(name, event_mgr, **kwargs)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.rx_qs = input_qs
        self.output_q = output_q
        self.clk = clk
        if self.clk is not None:
            self.clk.control_flow(self)
        if self.output_q is None:
            raise ValueError('output_q should be provided')
        for p in self.rx_qs:
            if p is not None:
                if not isinstance(p, SQQueue):
                    raise ValueError(f'queues should contain  SQQueue object ,'
                                     f' got {type(p)} instead.')

            else:
                raise ValueError('Null Queue Provided')
        self.helper = helper
        self.helper.set_owner(self)
        self.helper.set_rx_queues(self.rx_qs)
        self.current_port = None

    def process_packet(self, evt):
        super().process_packet(evt)
        if evt.owner is self.clk:
            self.current_port = self.helper.get_rx_q(self)
            if self.current_port is not None:
                curr_pkt = self.current_port.pop()
                if curr_pkt is not None:
                    self.output_q.push(copy.copy(curr_pkt))
                    self.finish_indication()
        else:
            if evt.name != f'{self.name}_start':
                self.logger.error(f'Ignoring Events other than Clock Events {evt}')

    def process_data(self, evt: SQEvent):
        super().process_data(evt)
        self.helper.process_data(evt)
