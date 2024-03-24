from .sq_object_abstract_factory import SQObjectAbstractFactory
from ..sq_simulator import SQSimulator
from ..sq_clock import SQClock
from ..sq_filter import SQFilter
from ..sq_mux_demux import  SQMux, SQDemux
from ..sq_merger import SQMerger
from ..sq_pkt_gen import SQPacketGenerator
from ..sq_pkt_processor import SQPktProcessor
from ..sq_pkt_sink import SQPktSink
from ..sq_queue import SQSingleQueue
from ..sq_splitter import SQSplitter


class SQDefaultObjectFactory(SQObjectAbstractFactory):
    def create_simulator(self, name, **kwargs):
        return SQSimulator(name=name,
                           event_mgr=self.evt_mgr,
                           **kwargs)

    def create_clock(self, name, **kwargs) -> SQClock:
        """
        Create a clock object
        :param name: Name of the object
        :param kwargs: Dictionary of other parameters
            clk_divider: Divider for the clock
        :return:
        """
        return SQClock(name=name, event_mgr=self.evt_mgr,  **kwargs)

    def create_filter(self, name, **kwargs) -> SQFilter:
        """
        Create a filter object
        :param name: Name of the object
        :param kwargs: Dictionary of other parameters
            clk: Clock to be used for timing
            input_q: Input Queue
            output_q: Output Queue
        :return:
        """
        filter_helper = self._helper_factory.create_filter_helper()
        return SQFilter(name=name, event_mgr=self.evt_mgr, helper=filter_helper, **kwargs)

    def create_merger(self, name, **kwargs) -> SQMerger:
        return SQMerger(name, self.evt_mgr, **kwargs)

    def create_mux(self, name, **kwargs) -> SQMux:
        mux_helper = self._helper_factory.create_mux_demux_helper()
        return SQMux(name=name,
                     event_mgr=self.evt_mgr,
                     helper=mux_helper, **kwargs)

    def create_demux(self, name, **kwargs) -> SQDemux:
        demux_helper = self._helper_factory.create_mux_demux_helper()
        return SQDemux(name=name,
                       event_mgr=self.evt_mgr,
                       helper=demux_helper, **kwargs)

    def create_packet_generator(self, name, **kwargs):
        pkt_gen_helper = self._helper_factory.create_pkt_gen_helper()
        return SQPacketGenerator(name=name,
                                 event_mgr=self.evt_mgr,
                                 helper=pkt_gen_helper, **kwargs)

    def create_packet_processor(self, name, **kwargs):
        pkt_processor_helper = self._helper_factory.create_pkt_processor_helper()
        return SQPktProcessor(name=name,
                              event_mgr=self.evt_mgr,
                              helper=pkt_processor_helper, **kwargs)

    def create_packet_sink(self, name, **kwargs):
        return SQPktSink(name=name, event_mgr=self.evt_mgr, **kwargs)

    def create_queue(self, name, **kwargs):
        return SQSingleQueue(name=name,
                             event_mgr=self.evt_mgr, **kwargs)

    def create_splitter(self, name, **kwargs):
        return SQSplitter(name=name,
                          event_mgr=self.evt_mgr, **kwargs)
