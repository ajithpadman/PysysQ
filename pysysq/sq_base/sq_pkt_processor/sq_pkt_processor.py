from typing import Union

from pysysq.sq_base import SQTimeBase
from pysysq.sq_base.sq_clock import SQClock
from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_packet.sq_metadata import SQMetadata
from pysysq.sq_base.sq_pkt_processor.sq_pkt_processor_helper import SQPktProcessorHelper
from pysysq.sq_base.sq_pkt_processor.sq_pkt_processor_state import SQPktProcState
from pysysq.sq_base.sq_pkt_processor.sq_random_pkt_processing_helper import SQRandomPktProcessingHelper
from pysysq.sq_base.sq_pkt_processor.sq_state_factory import SQStateFactory
from pysysq.sq_base.sq_queue import SQSingleQueue, SQQueue


class SQPktProcessor(SQObject):
    def __init__(self, name: str,
                 event_mgr,
                 clk: Union[SQClock, None],
                 input_q: Union[SQQueue, None],
                 helper: SQPktProcessorHelper,
                 **kwargs):
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
        self.clk = clk
        self.input_queue = input_q
        if not isinstance(self.input_queue, SQQueue):
            raise ValueError(f'Input Queue should be a SQ Queue')

        self.helper: SQPktProcessorHelper = helper
        self.helper.set_owner(self)
        self._state_factory = SQStateFactory()
        self._state = self._state_factory.create_state(name='IDLE', owner=self)
        self.processing_time = 0
        self.curr_pkt = None
        self.start_tick = 0
        self.no_of_processed_pkts = 0
        self.pkt_size_average = 0
        self.pkt_size_sum = 0
        self.avg_processing_time = 0
        self.total_processing_time = 0
        self.load = 0
        # self.register_property('no_of_processed_pkts')
        # self.register_property('pkt_size_average')
        # self.register_property('avg_processing_time')
        # self.register_property('state')
        self.register_property('load')
        self.clk.control_flow(self)

    def set_state(self, state: SQPktProcState):
        self._state = state

    def process_packet(self, evt):
        super().process_packet(evt)
        self.tick += 1
        if evt.owner is self.clk:
            self._state.process_packet(evt)

        else:
            self.logger.warning(f'{self.name} Ignoring Event {evt.data}')
