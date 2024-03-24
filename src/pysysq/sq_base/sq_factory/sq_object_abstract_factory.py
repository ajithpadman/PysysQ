from abc import ABC, abstractmethod
from ..sq_event import SQEventManager
from .sq_helper_abstract_factory import SQHelperAbstractFactory
from ..sq_simulator import SQSimulator
from ..sq_clock import SQClock
from ..sq_filter import SQFilter
from ..sq_mux_demux import SQMux, SQDemux
from ..sq_merger import SQMerger
from ..sq_pkt_gen import SQPacketGenerator
from ..sq_pkt_processor import SQPktProcessor
from ..sq_pkt_sink import SQPktSink
from ..sq_queue import SQQueue
from ..sq_splitter import SQSplitter


class SQObjectAbstractFactory(ABC):

    def __init__(self, helper_factory: SQHelperAbstractFactory):
        self._helper_factory = helper_factory
        self.evt_mgr = SQEventManager()

    @abstractmethod
    def create_simulator(self, name, **kwargs) -> SQSimulator:
        pass

    @abstractmethod
    def create_clock(self, name, **kwargs) -> SQClock:
        pass

    @abstractmethod
    def create_filter(self, name, **kwargs) -> SQFilter:
        pass

    @abstractmethod
    def create_merger(self, name, **kwargs) -> SQMerger:
        pass

    @abstractmethod
    def create_mux(self, name, **kwargs) -> SQMux:
        pass

    @abstractmethod
    def create_demux(self, name, **kwargs) -> SQDemux:
        pass

    @abstractmethod
    def create_packet_generator(self, name, **kwargs) -> SQPacketGenerator:
        pass

    @abstractmethod
    def create_packet_processor(self, name, **kwargs) -> SQPktProcessor:
        pass

    @abstractmethod
    def create_packet_sink(self, name, **kwargs)-> SQPktSink:
        pass

    @abstractmethod
    def create_queue(self, name, **kwargs)->SQQueue:
        pass

    @abstractmethod
    def create_splitter(self, name, **kwargs)->SQSplitter:
        pass
