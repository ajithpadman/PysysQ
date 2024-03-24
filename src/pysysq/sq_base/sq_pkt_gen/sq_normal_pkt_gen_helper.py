import numpy as np
from .sq_pkt_gen_helper import SQPktGenHelper
from ..sq_packet import SQPacket, SQPacketInfo
from ..sq_time_base import SQTimeBase



class SQNormalPktGenHelper(SQPktGenHelper):
    """
    This class is used to generate packets with
    normal distribution of packet size and number of packets.
    """

    def set_params(self, **kwargs):
        self.no_pkts_mean = kwargs.get('no_pkts_mean', 10)
        self.no_pkts_sd = kwargs.get('no_pkts_sd', 2)
        self.pkt_size_mean = kwargs.get('pkt_size_mean', 1000)
        self.pkt_size_sd = kwargs.get('pkt_size_sd', 2000)
        self.classes = kwargs.get('classes', ['A'])
        self.priorities = kwargs.get('priorities', (1, 10))

    def __init__(self):
        super().__init__()
        self.no_pkts_mean = 10
        self.no_pkts_sd = 2
        self.pkt_size_mean = 1000
        self.pkt_size_sd = 2000
        self.classes = ['A', 'B']
        self.priorities = (1, 10)
        self.pkt_id = 0

    def generate_pkts(self):
        pkts = []
        no_of_pkts = int(np.abs(np.random.normal(self.no_pkts_mean, self.no_pkts_sd, None)))
        pkt_sizes = [int(x) for x in np.abs(np.random.normal(self.pkt_size_mean, self.pkt_size_sd, no_of_pkts))]
        pkt_classes = np.random.choice(self.classes, no_of_pkts)
        pkt_priorities = np.random.randint(self.priorities[0], self.priorities[1], no_of_pkts)
        pkt_info: SQPacketInfo = SQPacketInfo(no_of_pkts, pkt_sizes, pkt_classes, pkt_priorities)
        for p in range(pkt_info.no_of_pkts):
            pkt = SQPacket(id=self.pkt_id,
                           size=pkt_info.pkt_sizes[p],
                           class_name=pkt_info.pkt_classes[p],
                           priority=pkt_info.pkt_priorities[p],
                           generation_time=SQTimeBase.get_current_sim_time())
            self.pkt_id += 1
            pkts.append(pkt)
        yield pkts
