from .sq_helper_abstract_factory import SQHelperAbstractFactory
from ..sq_filter import SQAllPassFilter
from ..sq_mux_demux import SQRRMuxDemuxHelper
from ..sq_pkt_gen import SQNormalPktGenHelper
from ..sq_pkt_processor import SQRandomPktProcessingHelper
class SQDefaultHelperFactory(SQHelperAbstractFactory):
    def create_filter_helper(self):
        return SQAllPassFilter()

    def create_mux_demux_helper(self):
        return SQRRMuxDemuxHelper()

    def create_pkt_gen_helper(self):
        return SQNormalPktGenHelper()

    def create_pkt_processor_helper(self):
        return SQRandomPktProcessingHelper()
