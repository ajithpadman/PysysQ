from typing import List, Union

from pysysq.sq_base.sq_mux_demux.sq_mux_demux_helper import SQMuxDemuxHelper
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_packet import SQPacket
from pysysq.sq_base.sq_packet.sq_metadata import SQMetadata
from pysysq.sq_base.sq_queue import SQQueue


class SQPktPrioQSelector(SQMuxDemuxHelper):
    def get_rx_q(self, requester: SQObject) -> SQQueue:
        # find the port with the highest priority packet
        max_priority = -1
        max_priority_port = None
        for port in self.rx_qs:
            if not port.is_empty():
                pkt = port.peek()
                if pkt.priority > max_priority:
                    max_priority = pkt.priority
                    max_priority_port = port
        selected_port = self.rx_qs.index(max_priority_port)
        metadata = SQMetadata(name='selected_port', owner=self.owner.name, value=selected_port)
        self.owner.data_indication(metadata)

        return max_priority_port

    def __init__(self):
        super().__init__()

    def get_tx_q(self, pkt: SQPacket, requester: SQObject) -> Union[SQQueue, None]:
        if pkt is None:
            return None
        selected_port = pkt.priority % len(self.tx_qs)
        metadata = SQMetadata(name='selected_port', owner=self.owner.name, value=selected_port)
        self.owner.data_indication(metadata)
        return self.tx_qs[selected_port]

    def process_data(self, evt):
        self.owner.logger.info(f'Consuming Metadata {evt.data.name} : {evt.data.value} from {evt.data.owner}')
