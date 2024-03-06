from typing import List, Dict, Union

from pysysq.sq_base.sq_packet import SQPacket
from pysysq.sq_base.sq_queue import SQQueue
from pysysq.sq_base.sq_queue.sq_q_selector import SQQueueSelector


class SQPktPriorityQSelector(SQQueueSelector):

    def __init__(self, queues: List[SQQueue]):
        super().__init__(queues)

    def get(self, pkt: SQPacket) -> Union[SQQueue, None]:
        if pkt is not None:
            return self.queue_list[pkt.priority % len(self.queue_list)]
        return None
