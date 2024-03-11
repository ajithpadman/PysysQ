import copy
from typing import List, Union

from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_mux_demux import SQMuxDemuxHelper
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_queue import SQQueue


class SQMux(SQObject):
    def __init__(self, name: str,
                 event_mgr,
                 rx_rqs: List[SQQueue],
                 output_q: Union[SQQueue, None],
                 helper: SQMuxDemuxHelper = None,
                 **kwargs):
        super().__init__(name, event_mgr, **kwargs)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.rx_qs = rx_rqs
        self.output_q = output_q
        if self.output_q is None:
            raise ValueError('output_q should be provided')
        for p in self.rx_qs:
            if p is not None:
                if not isinstance(p, SQQueue):
                    raise ValueError(f'queues should contain  SQQueue object ,'
                                     f' got {type(p)} instead.')
                else:
                    p.control_flow(self)
            else:
                raise ValueError('Null Queue Provided')
        self.helper = helper
        self.helper.set_rx_queues(self.rx_qs)
        self.current_port = 0

    def process_packet(self, evt):
        super().process_packet(evt)
        if evt.owner is not self:
            self.current_port = self.helper.get_rx_q(self)
            if self.current_port is not None:
                curr_pkt = self.current_port.pop()
                if curr_pkt is not None:
                    self.output_q.push(copy.copy(curr_pkt))
                    self.finish_indication()
        else:
            if evt.name != f'{self.name}_start':
                self.logger.error(f'Ignoring Self Event {evt}')
