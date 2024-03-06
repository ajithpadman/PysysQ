from pysysq.sq_base.sq_clock import SQClock
from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_pkt_processor.sq_pkt_processor_helper import SQPktProcessorHelper
from pysysq.sq_base.sq_pkt_processor.sq_random_pkt_processing_helper import SQRandomPktProcessingHelper
from pysysq.sq_base.sq_queue import SQSingleQueue, SQQueue


class SQPktProcessor(SQObject):
    def __init__(self, name: str, event_mgr, **kwargs):
        """
        Constructor for the SQPktProcessor
        :param name: Name of the Packet Processor
        :param event_mgr: Event Manager to be used
        :param kwargs: Dictionary of optional parameters
            clk: Clock to be used for timing
            input_queue: Queue from which the packets are received
            output_queue: Queue to which the processed packets are sent
            helper: Helper to be used for processing the packets.
            the helper should be a subclass of SQPktProcessorHelper
        """
        super().__init__(name, event_mgr, **kwargs)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.clk = kwargs.get('clk', SQClock(name=f'{self.name}_clk',
                                             event_mgr=event_mgr))
        self.input_queue: SQSingleQueue = kwargs.get('input_queue',
                                                     SQSingleQueue(name=f'{self.name}_input_queue',
                                                                   event_mgr=event_mgr))
        if not isinstance(self.input_queue, SQQueue):
            raise ValueError(f'Input Queue should be a SQ Queue')

        self.output_queue: SQSingleQueue = kwargs.get('output_queue',
                                                      SQSingleQueue(name=f'{self.name}_output_queue',
                                                                    event_mgr=event_mgr))
        if not isinstance(self.output_queue, SQQueue):
            raise ValueError(f'Output Queue should be a SQ Queue')

        self.helper: SQPktProcessorHelper = kwargs.get('helper',
                                                       SQRandomPktProcessingHelper(
                                                           owner=self,
                                                           name=SQRandomPktProcessingHelper.__name__)
                                                       )
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

            self.curr_pkt = self.input_queue.pop()
            self.start_tick = self.tick
            if self.curr_pkt is not None:
                self.state = 'PROCESSING'
                self.state_id = 1
                self.pkt_size_sum += self.curr_pkt.size
                self.pkt_size_average = self.pkt_size_sum / (self.no_of_processed_pkts + 1)
                self.processing_time = self.helper.get_processing_ticks(self.curr_pkt)
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
                evt.data = self.curr_pkt
                self.output_queue.process(evt)
                self.finish_indication()
            else:
                self.tick += 1
                metadata = self.helper.process_packet(self.curr_pkt, self.tick - self.start_tick)
                self.data_indication(data=metadata)
                self.logger.info(f'{self.name} Continue Processing Packet '
                                 f'{self.curr_pkt} Time {self.tick}')
        else:
            self.logger.warning(f'{self.name} Ignoring Event {evt.data}')
