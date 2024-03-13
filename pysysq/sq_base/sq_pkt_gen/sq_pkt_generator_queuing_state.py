from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_pkt_gen.sq_generator_state import SQPktGeneratorState


class SQPktGeneratorQueuingState(SQPktGeneratorState):
    def process_packet(self, evt: SQEvent):
        self.owner.output_q.push(self.owner.packets[self.owner.tick])
        self.owner.generated_pkts += 1
        self.owner.total_pkts += 1
        self.owner.logger.info(f'Packet {self.owner.packets[self.owner.tick]} Ready for Queuing')
        self.owner.tick += 1
        if self.owner.tick >= len(self.owner.packets):
            self.owner.packets = []
            self.owner.tick = 0
            self.owner.set_state(self.factory.create_state(name='GENERATING',owner=self.owner))
        self.owner.finish_indication()

    def get_state_name(self):
        return f'QUEUING'
