from pysysq.sq_base.sq_pkt_processor.sq_pkt_processor_helper import SQPktProcessorHelper
import numpy as np


class SQRandomPktProcessingHelper(SQPktProcessorHelper):

    def get_processing_ticks(self, pkt):
        if pkt.size <= 100:
            return np.random.randint(1, 3)
        elif pkt.size <= 200:
            return np.random.randint(2, 8)
        elif pkt.size <= 300:
            return np.random.randint(5, 10)
        else:
            return np.random.randint(10, 15)
