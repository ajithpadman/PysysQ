from pysysq.sq_base.sq_packet import SQPacketInfo, SQPacket
from pysysq.sq_base.sq_pkt_gen.sq_pkt_gen_helper import SQPktGenHelper
import numpy as np

from pysysq.sq_base import SQTimeBase


class SQPoissonPktGenHelper(SQPktGenHelper):
    def generate_pkts(self):
        pkts =[]
        no_of_pkts = np.random.poisson(self.rate, None)
        pkt_sizes = np.random.poisson(self.size, no_of_pkts)
        pkt_classes = np.random.choice(self.classes, no_of_pkts)
        pkt_priorities = np.random.randint(self.priorities[0], self.priorities[1], no_of_pkts)
        pkt_info: SQPacketInfo = SQPacketInfo(no_of_pkts, pkt_sizes, pkt_classes, pkt_priorities)
        for p in range(pkt_info.no_of_pkts):
            pkt = SQPacket(size=pkt_info.pkt_sizes[p],
                           class_name=pkt_info.pkt_classes[p],
                           priority=pkt_info.pkt_priorities[p],
                           arrival_time=SQTimeBase.get_current_sim_time())
            pkts.append(pkt)
        yield pkts

    def __init__(self, **kwargs):
        """
        Constructor for the SQPoissonPktGenHelper
        :param kwargs: Dictionary of optional parameters
            rate: Expected number of packets
            size: Expected Size of a packet
            classes: List of classes of packets  to choose from
            priorities: Tuple of priorities for packets
        """
        self.rate = kwargs.get('rate', 10)
        self.size = kwargs.get('size', 100)
        self.classes = kwargs.get('classes', ['A'])
        self.priorities = kwargs.get('priorities', (1, 10))
