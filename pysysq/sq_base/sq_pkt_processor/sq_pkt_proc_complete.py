from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_packet.sq_metadata import SQMetadata
from pysysq.sq_base.sq_pkt_processor.sq_pkt_processor_state import SQPktProcState


class SQPktProcStateComplete(SQPktProcState):
    def process_packet(self, evt: SQEvent):
        self.owner.no_of_processed_pkts += 1
        self.owner.total_processing_time += self.owner.processing_time
        self.owner.avg_processing_time = self.owner.total_processing_time / self.owner.no_of_processed_pkts
        self.owner.load = self.owner.total_processing_time / self.owner.tick * 100
        metadata = self.owner.helper.process_packet(self.owner.curr_pkt, self.owner.tick - self.owner.start_tick)
        progress = (self.owner.tick - self.owner.start_tick) / self.owner.processing_time * 100
        progress_metadata = SQMetadata(name='progress', owner=self.owner.name, value=progress)
        if metadata is not None:
            self.owner.data_indication(data=metadata)
        self.owner.data_indication(data=progress_metadata)
        self.owner.logger.info(f'{self.owner.name} Packet {self.owner.curr_pkt} Processing Complete after ticks '
                               f'{self.owner.tick}')
        self.owner.finish_indication(data=self.owner.curr_pkt)
        self.owner.set_state(self.factory.create_state('IDLE', owner=self.owner))

    def get_state_name(self):
        return f'COMPLETE'