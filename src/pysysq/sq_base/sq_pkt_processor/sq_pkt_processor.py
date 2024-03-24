from typing import Union

from ..sq_object import SQObject
from ..sq_clock import SQClock
from ..sq_queue import SQQueue
from .sq_pkt_processor_helper import SQPktProcessorHelper
from ..sq_logger import SQLogger
from .sq_state_factory import SQStateFactory
from .sq_pkt_processor_state import SQPktProcState
from ..sq_packet import SQMetadata
from ..sq_event import SQEvent


class SQPktProcessor(SQObject):
    def __init__(self, name: str,
                 event_mgr,
                 clk: Union[SQClock, None],
                 input_q: Union[SQQueue, None],
                 output_q: Union[SQQueue, None],
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
        self.output_queue = output_q
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
        if self.clk is not None:
            self.clk.control_flow(self)

    def set_state(self, state: SQPktProcState):
        self._state = state

    def process_packet(self, evt):
        super().process_packet(evt)
        if evt.owner is self.clk:
            self.tick += 1
            self._state.process_packet(evt)
        else:
            self.logger.warning(f'{self.name} Ignoring Event {evt.data}')

    def update_progress(self):
        progress = (self.tick - self.start_tick) / self.processing_time * 100
        progress_metadata = SQMetadata(name='progress', owner=self.name, value=progress)
        self.data_indication(data=progress_metadata)

    def process_data(self, evt: SQEvent):
        super().process_data(evt)
        self.helper.process_data(evt.data, self.tick)
