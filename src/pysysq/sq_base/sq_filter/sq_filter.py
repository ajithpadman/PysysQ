import copy
from ..sq_object import SQObject
from ..sq_filter import SQFilterHelper
from ..sq_clock import SQClock
from ..sq_queue import SQQueue
from ..sq_logger import SQLogger


class SQFilter(SQObject):
    def __init__(self, name: str,
                 event_mgr,
                 helper: SQFilterHelper,
                 clk: SQClock,
                 input_q: SQQueue,
                 output_q: SQQueue,
                 **kwargs):
        super().__init__(name, event_mgr, **kwargs)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.helper = helper
        self.helper.set_owner(self)
        self.input_q = input_q
        self.output_q = output_q
        self.clk = clk
        self.clk.control_flow(self)

    def process_packet(self, evt):
        super().process_packet(evt)
        if evt.owner is self.clk:
            pkt = self.input_q.pop()
            if pkt is not None:
                if self.helper.filter(pkt):
                    self.output_q.push(copy.copy(pkt))
                    self.finish_indication(data=evt.data)
        else:
            if evt.name != f'{self.name}_start':
                self.logger.error(f'Ignoring Events other than Clock Events {evt}')
