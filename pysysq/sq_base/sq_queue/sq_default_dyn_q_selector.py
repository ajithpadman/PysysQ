from pysysq.sq_base.sq_packet import SQPacket
from pysysq.sq_base.sq_queue.sq_dyn_q_selector import SQDynQSelector


class SQDefaultDynQSelector(SQDynQSelector):
    def get(self, pkt: SQPacket):
        return pkt.priority
