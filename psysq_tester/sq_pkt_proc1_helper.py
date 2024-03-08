
from pysysq.sq_base.sq_pkt_processor import SQPktProcessorHelper


class SQPktProc1Helper(SQPktProcessorHelper):
    def __init__(self, name: str):
        super().__init__(name)

    def get_processing_ticks(self, pkt):
        return 5

    def process_packet(self, pkt, time):
        return None
