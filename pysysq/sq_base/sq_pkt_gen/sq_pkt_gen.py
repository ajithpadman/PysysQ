from pysysq.sq_base.sq_clock import  SQClock
from pysysq.sq_base.sq_queue import SQQueue
from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_event.sq_event_manager import SQEventManager
from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_pkt_gen.sq_generator_state import SQPktGeneratorState
from pysysq.sq_base.sq_pkt_gen.sq_generator_state_factory import SQGeneratorStateFactory
from pysysq.sq_base.sq_pkt_gen.sq_normal_pkt_gen_helper import SQNormalPktGenHelper
from pysysq.sq_base.sq_pkt_gen.sq_pkt_gen_helper import SQPktGenHelper
from pysysq.sq_base.sq_pkt_gen.sq_pkt_generator_gen_state import SQPktGeneratorGenState


class SQPacketGenerator(SQObject):
    """
    Base class for all Packet Generators in the simulation
    The class implements the basic functionality of a packet generator
    """

    def __init__(self, name: str,
                 event_mgr: SQEventManager,
                 helper: SQPktGenHelper,
                 output_q: SQQueue,
                 clk: SQClock,
                 **kwargs):

        super().__init__(name, event_mgr, **kwargs)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.state: SQPktGeneratorState = SQPktGeneratorGenState(owner=self, factory=SQGeneratorStateFactory())
        self.generated_pkts = 0
        self.total_pkts = 0
        self.output_q = output_q
        self.clk = clk
        if self.clk is not None:
            self.clk.control_flow(self)
        self.helper: SQPktGenHelper = helper
        self.helper.set_owner(self)
        self.helper.set_params(**kwargs)
        if not isinstance(self.helper, SQPktGenHelper):
            raise ValueError("Packet Generator Helper must be derived from SQPktGenHelper")
        self.register_property('generated_pkts')
        self.register_property('total_pkts')
        self.packets = []

    def set_state(self, state):
        self.state = state

    def process_packet(self, evt: SQEvent):
        super().process_packet(evt)
        if evt.owner is self.clk:
            self.state.process_packet(evt)
        else:
            if evt.name != f'{self.name}_start':
                self.logger.error(f'Ignoring Events other than Clock Events {evt}')
