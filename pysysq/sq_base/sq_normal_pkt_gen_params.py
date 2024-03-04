import numpy as np

from pysysq.sq_base.sq_packet_info import SQPacketInfo
from pysysq.sq_base.sq_object_params import SQObjectParams


class SQNormalPktGenParams(SQObjectParams):
    def __init__(self, no_pkts_mean, no_pkts_sd,pkt_size_mean,pkt_size_sd, classes: [str], priorities: (int, int)):
        self.no_pkts_mean = no_pkts_mean
        self.no_pkts_sd = no_pkts_sd
        self.pkt_size_mean = pkt_size_mean
        self.pkt_size_sd = pkt_size_sd
        self.classes = classes
        self.priorities = priorities

    def get_packet_data(self) -> SQPacketInfo:
        no_of_pkts = int(np.abs(np.random.normal(self.no_pkts_mean, self.no_pkts_sd, None)))
        pkt_sizes = [int(x) for x in np.abs(np.random.normal(self.pkt_size_mean, self.pkt_size_sd, no_of_pkts))]
        pkt_classes = np.random.choice(self.classes, no_of_pkts)
        pkt_priorities = np.random.randint(self.priorities[0], self.priorities[1], no_of_pkts)
        yield SQPacketInfo(no_of_pkts, pkt_sizes, pkt_classes, pkt_priorities)
