import copy

from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_mux_demux.sq_pkt_prio_q_selector import SQPktPrioQSelector
from pysysq.sq_base.sq_mux_demux.sq_rr_q_selector import SQRRQueueSelector
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_queue import SQSingleQueue, SQQueue


class SQMux(SQObject):
    def __init__(self, name: str, event_mgr, **kwargs):
        super().__init__(name, event_mgr, **kwargs)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.no_of_qs = kwargs.get('no_of_queues', 2)
        self.rx_qs = kwargs.get('queues', [SQSingleQueue(name=f'{name}_Q_{i}', event_mgr=event_mgr, **kwargs)
                                           for i in
                                           range(self.no_of_qs)])
        self.output_q = kwargs.get('output_q', SQSingleQueue(name=f'{name}_Output', event_mgr=event_mgr, **kwargs))
        for p in self.rx_qs:
            if not isinstance(p, SQQueue):
                raise ValueError(f'queues should contain  SQQueue object , got {type(p)} instead.')
            p.control_flow(self)
        self.helper = kwargs.get('helper', SQRRQueueSelector(self.rx_qs))
        self.current_port = 0

    def process(self, evt):
        super().process(evt)
        if evt.owner is not self:
            self.current_port = self.helper.get_tx_q(self)
            if self.current_port is not None:
                curr_pkt = self.current_port.pop()
                if curr_pkt is not None:
                    self.output_q.push(copy.copy(curr_pkt))
                    self.finish_indication()



        else:
            if evt.name != f'{self.name}_start':
                self.logger.error(f'Ignoring Self Event {evt}')
