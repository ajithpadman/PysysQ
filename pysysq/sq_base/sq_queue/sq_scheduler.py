from typing import List, Union

from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_queue import SQQueue


class SQScheduler:
    def __init__(self, queues: List[SQQueue]):
        self.queue_list = queues

    def get(self, requester: SQObject) -> Union[SQQueue, None]:
        pass
