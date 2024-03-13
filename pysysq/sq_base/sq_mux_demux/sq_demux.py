import copy
from typing import List, Union

from pysysq.sq_base.sq_clock import SQClock
from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_mux_demux import SQMuxDemuxHelper
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_queue import SQQueue


class SQDemux(SQObject):
    def __init__(self, name: str,
                 event_mgr,
                 output_qs: List[SQQueue],
                 input_q: Union[SQQueue, None],
                 clk: SQClock,
                 helper: SQMuxDemuxHelper,
                 **kwargs):
        super().__init__(name, event_mgr, **kwargs)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.tx_qs = output_qs
        self.input_q = input_q
        self.clk = clk
        if self.clk is not None:
            self.clk.control_flow(self)
        else:
            raise ValueError('input_q should be provided')
        for p in self.tx_qs:
            if not isinstance(p, SQQueue):
                raise ValueError(f'queues should contain SQQueue, got {type(p)} instead.')

        self.helper = helper
        self.helper.set_owner(self)
        self.helper.set_tx_queues(self.tx_qs)
        self.current_port = 0

    def process_packet(self, evt):
        super().process_packet(evt)
        if evt.owner is self.clk:
            curr_pkt = self.input_q.pop()
            self.current_port = self.helper.get_tx_q(curr_pkt, self)
            if self.current_port is not None:
                if curr_pkt is not None:
                    self.current_port.push(copy.copy(curr_pkt))
                    self.finish_indication()
            else:
                self.logger.error(f'No Queue Selected for {evt.data}')
        else:
            if evt.name != f'{self.name}_start':
                self.logger.error(f'Ignoring Events other than clk events {evt}')

    def process_data(self, evt: SQEvent):
        super().process_data(evt)
        self.helper.process_data(evt)
