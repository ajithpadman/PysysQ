import numpy as np
from .sq_pkt_gen_helper import SQPktGenHelper
from ..sq_packet import SQPacket, SQPacketInfo
from ..sq_time_base import SQTimeBase


class SQPoissonPktGenHelper(SQPktGenHelper):
    def set_params(self, **kwargs):
        self.rate = kwargs.get('rate', 10)
        self.size = kwargs.get('size', 100)
        self.classes = kwargs.get('classes', ['A'])
        self.priorities = kwargs.get('priorities', (1, 10))

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
                           generation_time=SQTimeBase.get_current_sim_time())
            pkts.append(pkt)
        yield pkts

    def __init__(self):
        super().__init__()
        self.rate = 10
        self.size = 100
        self.classes = ['A']
        self.priorities = (1, 10)
