from typing import List, Union

from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_queue import SQQueue
from pysysq.sq_base.sq_queue.sq_scheduler import SQScheduler


class SQRRScheduler(SQScheduler):
    def __init__(self, queues: List[SQQueue]):
        super().__init__(queues=queues)
        self.current_queue = 0

    def get(self, requester: SQObject) -> Union[SQQueue, None]:
        queue = self.queue_list[self.current_queue]
        self.current_queue += 1
        if self.current_queue >= len(self.queue_list):
            self.current_queue = (self.current_queue % len(self.queue_list))
        return queue
