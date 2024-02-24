import logging
from typing import List, Union

from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_event_queue import SQEventQueue
from pysysq.sq_base.sq_time_base import SQTimeBase


class SQEventManager:
    def __init__(self):
        self.event_queue_list: List[SQEventQueue] = []

    def schedule(self, _event: SQEvent, when: int):
        logging.info(f'SQEventManager:Schedule Event {_event.name} after {when} sim time')
        queue = self.get_event_queue(_event.owner.params.evt_q)
        if queue is not None:
            queue.schedule(_event=_event)
            _event.scheduled_tick = when + SQTimeBase.get_current_sim_time()

    def get_event_queue(self, index: int) -> Union[SQEventQueue, None]:
        queue: Union[SQEventQueue, None] = None
        if self.event_queue_list is not None:
            if len(self.event_queue_list) > index:
                queue = self.event_queue_list[index]
            else:
                queue = SQEventQueue()
                self.event_queue_list.append(queue)
        return queue

    def run(self):

        for queue in self.event_queue_list:
            if queue.get_next_event() is not None:
                next_evt = queue.pop_next_event()
                for action in next_evt.actions:
                    action()

