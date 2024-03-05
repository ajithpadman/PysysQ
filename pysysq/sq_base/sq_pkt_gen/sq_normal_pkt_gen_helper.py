from pysysq.sq_base.sq_packet import SQPacketInfo, SQPacket
from pysysq.sq_base.sq_pkt_gen.sq_pkt_gen_helper import SQPktGenHelper
import numpy as np

from pysysq.sq_base import SQTimeBase


class SQNormalPktGenHelper(SQPktGenHelper):
    """
    This class is used to generate packets with
    normal distribution of packet size and number of packets.
    """
    def __init__(self, **kwargs):
        """
        Constructor for the SQNormalPktGenHelper
        :param kwargs: Dictionary of optional parameters
            no_pkts_mean: Mean of the number of packets
            no_pkts_sd: Standard deviation of the number of packets
            pkt_size_mean: Mean of the packet size
            pkt_size_sd: Standard deviation of the packet size
            classes: List of classes of packets  to choose from
            priorities: Tuple of priorities for packets
        """
        self.no_pkts_mean = kwargs.get('no_pkts_mean', 10)
        self.no_pkts_sd = kwargs.get('no_pkts_sd', 2)
        self.pkt_size_mean = kwargs.get('pkt_size_mean', 100)
        self.pkt_size_sd = kwargs.get('pkt_size_sd', 20)
        self.classes = kwargs.get('classes', ['A'])
        self.priorities = kwargs.get('priorities', (1, 10))

    def generate_pkts(self):
        pkts = []
        no_of_pkts = int(np.abs(np.random.normal(self.no_pkts_mean, self.no_pkts_sd, None)))
        pkt_sizes = [int(x) for x in np.abs(np.random.normal(self.pkt_size_mean, self.pkt_size_sd, no_of_pkts))]
        pkt_classes = np.random.choice(self.classes, no_of_pkts)
        pkt_priorities = np.random.randint(self.priorities[0], self.priorities[1], no_of_pkts)
        pkt_info:SQPacketInfo = SQPacketInfo(no_of_pkts, pkt_sizes, pkt_classes, pkt_priorities)
        for p in range(pkt_info.no_of_pkts):
            pkt = SQPacket(size=pkt_info.pkt_sizes[p],
                           class_name=pkt_info.pkt_classes[p],
                           priority=pkt_info.pkt_priorities[p],
                           arrival_time=SQTimeBase.get_current_sim_time())
            pkts.append(pkt)
        yield pkts

