from typing import Union
import numpy as np
from .sq_pkt_processor_helper import SQPktProcessorHelper
from ..sq_packet import SQMetadata


class SQRandomPktProcessingHelper(SQPktProcessorHelper):

    def process_data(self, data: SQMetadata, tick: int):
        self.owner.logger.info(f'Consuming Metadata {data}')

    def process_packet(self, pkt, tick: int) -> Union[SQMetadata, None]:
        self.owner.logger.info(f'Processing packet {pkt} at tick {tick}')
        if tick < self.get_processing_ticks(pkt):
            return None
        return SQMetadata(name='tick_count', owner=self.owner.name, value=tick)

    def get_processing_ticks(self, pkt):
        np.random.seed(pkt.size)
        return np.random.randint(1, 10)
