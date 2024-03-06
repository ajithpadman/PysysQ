from pysysq.sq_base.sq_packet.sq_metadata import SQMetadata
from pysysq.sq_base.sq_pkt_processor.sq_pkt_processor_helper import SQPktProcessorHelper
import numpy as np


class SQRandomPktProcessingHelper(SQPktProcessorHelper):

    def process_packet(self, pkt, tick: int):
        self.owner.logger.debug(f'Processing packet {pkt} at tick {tick} by {self.name}')
        if tick < self.get_processing_ticks(pkt):
            return None
        return SQMetadata(name='metadata1', value=not self.owner.metadata.get('metadata1', False))

    def get_processing_ticks(self, pkt):
        if pkt.size <= 100:
            return np.random.randint(1, 3)
        elif pkt.size <= 200:
            return np.random.randint(2, 8)
        elif pkt.size <= 300:
            return np.random.randint(5, 10)
        else:
            return np.random.randint(10, 15)
