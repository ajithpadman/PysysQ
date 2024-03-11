from abc import ABC, abstractmethod

from pysysq.sq_base.sq_clock import SQClock
from pysysq.sq_base.sq_event import SQEventManager
from pysysq.sq_base.sq_factory.sq_helper_abstract_factory import SQHelperAbstractFactory
from pysysq.sq_base.sq_filter import SQFilter
from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_merger import SQMerger
from pysysq.sq_base.sq_mux_demux import SQMux, SQDemux


class SQObjectAbstractFactory(ABC):

    def __init__(self, helper_factory: SQHelperAbstractFactory):
        self._helper_factory = helper_factory
        self.evt_mgr = SQEventManager()

    @abstractmethod
    def create_simulator(self, name, **kwargs):
        pass

    @abstractmethod
    def create_clock(self, name,  **kwargs) -> SQClock:
        pass

    @abstractmethod
    def create_filter(self, name,  **kwargs) -> SQFilter:
        pass

    @abstractmethod
    def create_merger(self, name,  **kwargs) -> SQMerger:
        pass

    @abstractmethod
    def create_mux(self, name, **kwargs) -> SQMux:
        pass

    @abstractmethod
    def create_demux(self, name,  **kwargs) -> SQDemux:
        pass

    @abstractmethod
    def create_packet_generator(self, name,  **kwargs):
        pass

    @abstractmethod
    def create_packet_processor(self, name,  **kwargs):
        pass

    @abstractmethod
    def create_packet_sink(self, name,  **kwargs):
        pass

    @abstractmethod
    def create_queue(self, name,  **kwargs):
        pass

    @abstractmethod
    def create_splitter(self, name,  **kwargs):
        pass
