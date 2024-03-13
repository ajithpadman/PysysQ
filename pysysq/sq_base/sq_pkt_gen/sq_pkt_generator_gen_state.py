from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_pkt_gen.sq_generator_state import SQPktGeneratorState


class SQPktGeneratorGenState(SQPktGeneratorState):
    def process_packet(self, evt: SQEvent):
        self.owner.generated_pkts = 0
        self.owner.logger.info(f'Generating Packets')
        self.owner.packets = [d for d in self.owner.helper.generate_pkts()][0]
        self.owner.logger.info(f'Generated {len(self.owner.packets)} Packets')
        self.owner.set_state(self.factory.create_state(name='QUEUING', owner=self.owner))

    def get_state_name(self):
        return f'GENERATING'
