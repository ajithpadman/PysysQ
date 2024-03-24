from pysysq.sq_base.sq_factory.sq_helper_abstract_factory import SQHelperAbstractFactory
from pysysq.sq_base.sq_filter.sq_pass_all_filter import SQAllPassFilter
from pysysq.sq_base.sq_mux_demux.sq_rr_mux_demux_helper import SQRRMuxDemuxHelper
from pysysq.sq_base.sq_pkt_gen import SQNormalPktGenHelper
from pysysq.sq_base.sq_pkt_processor.sq_random_pkt_processing_helper import SQRandomPktProcessingHelper


class SQDefaultHelperFactory(SQHelperAbstractFactory):
    def create_filter_helper(self):
        return SQAllPassFilter()

    def create_mux_demux_helper(self):
        return SQRRMuxDemuxHelper()

    def create_pkt_gen_helper(self):
        return SQNormalPktGenHelper()

    def create_pkt_processor_helper(self):
        return SQRandomPktProcessingHelper()
