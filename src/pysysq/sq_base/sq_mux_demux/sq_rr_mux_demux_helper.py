from typing import List
from .sq_mux_demux_helper import SQMuxDemuxHelper
from ..sq_packet import SQPacket
from ..sq_packet import SQMetadata
from ..sq_object import SQObject
from ..sq_queue import SQQueue


class SQRRMuxDemuxHelper(SQMuxDemuxHelper):
    def __init__(self, ):
        super().__init__()
        self.current_tx_queue_id = 0
        self.current_rx_queue_id = 0

    def get_tx_q(self, pkt: SQPacket, requester: SQObject) -> SQQueue:
        cur_q = self.tx_qs[self.current_tx_queue_id]
        selected_port = self.tx_qs.index(cur_q)
        metadata = SQMetadata(name='selected_port', owner=self.owner.name, value=selected_port)
        self.owner.data_indication(metadata)
        self.current_tx_queue_id += 1
        if self.current_tx_queue_id >= len(self.tx_qs):
            self.current_tx_queue_id = 0
        return cur_q

    def get_rx_q(self, requester: SQObject) -> SQQueue:
        cur_q = self.rx_qs[self.current_rx_queue_id]
        selected_port = self.rx_qs.index(cur_q)
        metadata = SQMetadata(name='selected_port', owner=self.owner.name, value=selected_port)
        self.owner.data_indication(metadata)
        self.current_rx_queue_id += 1
        if self.current_rx_queue_id >= len(self.rx_qs):
            self.current_rx_queue_id = 0
        return cur_q

    def process_data(self, evt):
        self.owner.logger.info(f'Consuming Metadata {evt.data.name} : {evt.data.value} from {evt.data.owner}')
