from pysysq.sq_base.sq_object_params import SQObjectParams
import numpy as np

from pysysq.sq_base.sq_packet_info import SQPacketInfo


class SQPoissonPktGenParams(SQObjectParams):
    def __init__(self, rate: float, size: float, classes: [str], priorities: (int, int)):
        self.rate = rate
        self.size = size
        self.classes = classes
        self.priorities = priorities

    def get_packet_data(self) -> SQPacketInfo:
        no_of_pkts = np.random.poisson(self.rate, None)
        pkt_sizes = np.random.poisson(self.size, no_of_pkts)
        pkt_classes = np.random.choice(self.classes, no_of_pkts)
        pkt_priorities = np.random.randint(self.priorities[0], self.priorities[1], no_of_pkts)
        yield SQPacketInfo(no_of_pkts, pkt_sizes, pkt_classes, pkt_priorities)
