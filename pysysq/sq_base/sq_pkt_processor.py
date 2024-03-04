import logging

from pysysq.logging_ctx import SIMLoggingCtx
from pysysq.sq_base.sq_clock import SQClock
from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_queue import SQQueue
from pysysq.sq_base.sq_statistics import SQStatisticsEntry


class SQPktProcessor(SQObject):
    def __init__(self, name: str, params, event_mgr, event_q: int = 1):
        super().__init__(name, params, event_mgr, event_q)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.clk = self.params.clk
        self.queue: SQQueue = self.params.queue
        self.state = 'IDLE'
        self.state_id = 0
        self.processing_time = 0
        self.curr_pkt = None
        self.start_tick = 0
        self.no_of_processed_pkts = 0
        self.pkt_size_average = 0
        self.pkt_size_sum = 0
        self.avg_processing_time = 0
        self.total_processing_time = 0
        self.register_property('no_of_processed_pkts')
        self.register_property('pkt_size_average')
        self.register_property('avg_processing_time')
        self.register_property('state_id')


    def process(self, evt):
        super().process(evt)
        if evt.owner is self.clk and self.state == 'IDLE':

            self.curr_pkt = self.queue.pop()
            self.start_tick = self.tick
            if self.curr_pkt is not None:
                self.state = 'PROCESSING'
                self.state_id = 1
                self.pkt_size_sum += self.curr_pkt.size
                self.pkt_size_average = self.pkt_size_sum / (self.no_of_processed_pkts + 1)
                self.processing_time = self.params.calculate_service_ticks(self.curr_pkt)
                self.logger.info(f'{self.name} Start Processing Packet '
                                 f'{self.curr_pkt} Expected processing time '
                                 f'{self.processing_time} current Tick {self.tick}')
            else:
                self.logger.info(f'{self.name} No Packet to Process')
        elif evt.owner is self.clk and self.state == 'PROCESSING':
            if self.tick >= (self.start_tick + self.processing_time):
                self.no_of_processed_pkts += 1
                self.total_processing_time += self.processing_time
                self.avg_processing_time = self.total_processing_time / self.no_of_processed_pkts
                self.logger.info(f'{self.name} Packet {self.curr_pkt} Processing Complete after ticks {self.tick}')
                self.state = 'IDLE'
                self.state_id = 0
                self.finish_indication()
            else:
                self.tick += 1
                self.logger.info(f'{self.name} Continue Processing Packet '
                                 f'{evt.data} Time {self.tick}')
        else:
            self.logger.warning(f'{self.name} Ignoring Event {evt.data}')
