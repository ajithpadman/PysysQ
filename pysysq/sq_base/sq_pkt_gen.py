import logging

from pysysq.logging_ctx import SIMLoggingCtx
from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_event_manager import SQEventManager
from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_packet import SQPacket
from pysysq.sq_base.sq_packet_info import SQPacketInfo
from pysysq.sq_base.sq_time_base import SQTimeBase


class SQPacketGenerator(SQObject):
    def __init__(self, name: str, params, event_mgr: SQEventManager):
        super().__init__(name, params, event_mgr)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.state = 'IDLE'
        self.generated_pkts = 0
        self.total_pkts = 0
        self.register_property('generated_pkts')
        self.register_property('total_pkts')
        self.packets = []

    def process(self, evt: SQEvent):
        super().process(evt)
        if self.state == 'IDLE':
            self.generated_pkts = 0
            self.logger.info(f'Generating Packets')
            self.state = 'GENERATING'
            pkt_info: SQPacketInfo = [p for p in self.params.get_packet_data()][0]
            for p in range(pkt_info.no_of_pkts):
                pkt = SQPacket(size=pkt_info.pkt_sizes[p],
                               class_name=pkt_info.pkt_classes[p],
                               priority=pkt_info.pkt_priorities[p],
                               arrival_time=SQTimeBase.get_current_sim_time())
                self.packets.append(pkt)
                self.logger.info(f'Packet {pkt} Generated')

            self.state = "QUEUING"
        elif self.state == 'QUEUING':
            self.finish_evt.data = self.packets[self.tick]
            self.generated_pkts += 1
            self.total_pkts += 1
            self.logger.info(f'Packet {self.packets[self.tick]} Ready for Queuing')
            self.tick += 1
            if self.tick >= len(self.packets):
                self.packets = []
                self.tick = 0
                self.state = 'IDLE'
            self.finish_indication()
