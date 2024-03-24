from ..sq_object import SQObject
from ..sq_clock import SQClock
from ..sq_queue import SQQueue
from ..sq_event import SQEvent
from ..sq_logger import SQLogger


class SQPktSink(SQObject):
    def __init__(self, name: str, event_mgr, input_q: SQQueue, clk: SQClock, **kwargs):
        super().__init__(name, event_mgr, **kwargs)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.input_q = input_q
        self.clk = clk
        if self.clk is not None:
            self.clk.control_flow(self)
        else:
            raise ValueError('Clock should be provided')

    def process_packet(self, evt: SQEvent):
        super().process_packet(evt)
        if evt.owner is self.clk:
            curr_pkt = self.input_q.pop()
            self.tick += 1
            if curr_pkt is not None:
                self.logger.info(f' Terminated the Packet {curr_pkt} path of the packet {curr_pkt.path} ')
            else:
                self.logger.info(f' No Packet to Terminate')
        else:
            if evt.name != f'{self.name}_start':
                self.logger.error(f'Ignoring Events other than Clock Events {evt}')
