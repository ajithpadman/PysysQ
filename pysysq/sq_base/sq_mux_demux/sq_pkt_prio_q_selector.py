from typing import List

from pysysq.sq_base.sq_mux_demux.sq_q_selector import SQQueueSelector
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_packet import SQPacket
from pysysq.sq_base.sq_queue import SQQueue


class SQPktPrioQSelector(SQQueueSelector):
    def get_tx_q(self, requester: SQObject) -> SQQueue:
        # find the port with the highest priority packet
        max_priority = -1
        max_priority_port = None
        for port in self.q_list:
            if not port.is_empty():
                pkt = port.peek()
                if pkt.priority > max_priority:
                    max_priority = pkt.priority
                    max_priority_port = port
        return max_priority_port

    def __init__(self, queues: List[SQQueue]):
        super().__init__(queues=queues)

    def get_rx_q(self, pkt: SQPacket, requester: SQObject) -> SQQueue:
        if pkt is None:
            return None
        return self.q_list[pkt.priority % len(self.q_list)]
