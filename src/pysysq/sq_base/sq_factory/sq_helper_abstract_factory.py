from abc import ABC, abstractmethod


class SQHelperAbstractFactory(ABC):
    @abstractmethod
    def create_filter_helper(self, **kwargs):
        pass

    @abstractmethod
    def create_mux_demux_helper(self, **kwargs):
        pass

    @abstractmethod
    def create_pkt_gen_helper(self, **kwargs):
        pass

    @abstractmethod
    def create_pkt_processor_helper(self, **kwargs):
        pass

