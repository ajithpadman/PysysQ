import copy
from typing import List, Union

from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_mux_demux import SQMuxDemuxHelper
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_queue import SQQueue


class SQDemux(SQObject):
    def __init__(self, name: str,
                 event_mgr,
                 tx_qs: List[SQQueue],
                 input_q: Union[SQQueue, None],
                 helper: SQMuxDemuxHelper,
                 **kwargs):
        super().__init__(name, event_mgr, **kwargs)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.tx_qs = tx_qs
        self.input_q = input_q
        if self.input_q is not None:
            self.input_q.control_flow(self)
        else:
            raise ValueError('input_q should be provided')
        for p in self.tx_qs:
            if not isinstance(p, SQQueue):
                raise ValueError(f'queues should contain SQQueue, got {type(p)} instead.')

        self.helper = helper
        self.helper.set_tx_queues(self.tx_qs)
        self.current_port = 0

    def process_packet(self, evt):
        super().process_packet(evt)
        if evt.owner is not self:
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
                self.logger.error(f'Ignoring Self Event {evt}')