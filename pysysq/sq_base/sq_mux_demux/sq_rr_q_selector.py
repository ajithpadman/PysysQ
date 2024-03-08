from typing import List

from pysysq.sq_base.sq_mux_demux import SQQueueSelector
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_packet import SQPacket
from pysysq.sq_base.sq_queue import SQQueue


class SQRRQueueSelector(SQQueueSelector):
    def __init__(self, queues: List[SQQueue]):
        super().__init__(queues=queues)
        self.current_tx_queue_id = 0
        self.current_rx_queue_id = 0

    def get_tx_q(self, requester: SQObject) -> SQQueue:
        cur_q = self.q_list[self.current_tx_queue_id]
        self.current_tx_queue_id += 1
        if self.current_tx_queue_id >= len(self.q_list):
            self.current_tx_queue_id = 0
        return cur_q

    def get_rx_q(self, pkt: SQPacket, requester: SQObject) -> SQQueue:
        cur_q = self.q_list[self.current_rx_queue_id]
        self.current_rx_queue_id += 1
        if self.current_rx_queue_id >= len(self.q_list):
            self.current_rx_queue_id = 0
        return cur_q
