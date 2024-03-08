import copy

from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_mux_demux.sq_pkt_prio_q_selector import SQPktPrioQSelector
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_queue import SQSingleQueue, SQQueue


class SQDemux(SQObject):
    def __init__(self, name: str, event_mgr, **kwargs):
        super().__init__(name, event_mgr, **kwargs)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.no_of_qs = kwargs.get('no_of_queues', 2)
        self.queues = kwargs.get('queues', [SQSingleQueue(name=f'{name}_Q_{i}', event_mgr=event_mgr, **kwargs)
                                            for i in
                                            range(self.no_of_qs)])
        self.input_q = kwargs.get('input_q', SQSingleQueue(name=f'{name}_Input', event_mgr=event_mgr, **kwargs))

        for p in self.queues:
            if not isinstance(p, SQQueue):
                raise ValueError(f'queues should contain SQQueue, got {type(p)} instead.')

        self.helper = kwargs.get('helper', SQPktPrioQSelector(self.queues))
        self.current_port = 0

    def process(self, evt):
        super().process(evt)
        if evt.owner is not self:
            curr_pkt = self.input_q.pop()
            self.current_port = self.helper.get_rx_q(curr_pkt, self)
            if self.current_port is not None:
                if curr_pkt is not None:
                    self.current_port.push(copy.copy(curr_pkt))
                    self.finish_indication()
            else:
                self.logger.error(f'No Queue Selected for {evt.data}')
        else:
            if evt.name != f'{self.name}_start':
                self.logger.error(f'Ignoring Self Event {evt}')
