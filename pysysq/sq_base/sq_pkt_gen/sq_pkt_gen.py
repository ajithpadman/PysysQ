from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_event.sq_event_manager import SQEventManager
from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_pkt_gen.sq_normal_pkt_gen_helper import SQNormalPktGenHelper
from pysysq.sq_base.sq_pkt_gen.sq_pkt_gen_helper import SQPktGenHelper


class SQPacketGenerator(SQObject):
    """
    Base class for all Packet Generators in the simulation
    The class implements the basic functionality of a packet generator
    """
    def __init__(self, name: str, event_mgr: SQEventManager, **kwargs):
        """
        Constructor for the SQPacketGenerator
        :param name: Name of the Packet Generator
        :param event_mgr: Event manager to be used
        :param kwargs: Dictionary of optional parameters
            helper: Helper class to be used for packet generation.
            This class must implement the abstract class SQPktGenHelper
        """
        super().__init__(name, event_mgr, **kwargs)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.state = 'IDLE'
        self.generated_pkts = 0
        self.total_pkts = 0
        self.helper: SQPktGenHelper = kwargs.get('helper', SQNormalPktGenHelper(**kwargs))
        if not isinstance(self.helper, SQPktGenHelper):
            raise ValueError("Packet Generator Helper must be derived from SQPktGenHelper")
        self.register_property('generated_pkts')
        self.register_property('total_pkts')
        self.packets = []

    def process(self, evt: SQEvent):
        super().process(evt)
        if self.state == 'IDLE':
            self.generated_pkts = 0
            self.logger.info(f'Generating Packets')
            self.state = 'GENERATING'
            self.packets = [d for d in self.helper.generate_pkts()][0]
            self.logger.info(f'Generated {len(self.packets)} Packets')
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
