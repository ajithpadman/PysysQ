from typing import Union

from pysysq.sq_base.sq_packet.sq_metadata import SQMetadata
from pysysq.sq_base.sq_pkt_processor.sq_pkt_processor_helper import SQPktProcessorHelper
import numpy as np


class SQRandomPktProcessingHelper(SQPktProcessorHelper):

    def process_data(self, data: SQMetadata, tick: int):
        self.owner.logger.debug(f'Consuming Metadata {data}')

    def process_metadata(self, metadata: SQMetadata):
        pass

    def process_packet(self, pkt, tick: int) -> Union[SQMetadata, None]:
        self.owner.logger.debug(f'Processing packet {pkt} at tick {tick}')
        if tick < self.get_processing_ticks(pkt):
            return None
        return SQMetadata(name='tick_count', owner=self.owner.name, value=tick)

    def get_processing_ticks(self, pkt):
        np.random.seed(pkt.size)
        return np.random.randint(1, 10)
