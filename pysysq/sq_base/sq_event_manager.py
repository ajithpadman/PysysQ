import logging
from typing import List, Union

from pysysq.logging_ctx import SIMLoggingCtx
from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_event_queue import SQEventQueue
from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_time_base import SQTimeBase


class SQEventManager:
    def __init__(self, name: str = ""):
        self.name = name
        self.event_queue_list: List[SQEventQueue] = []
        self.schedule_queue: List[SQEvent] = []
        self.logger = SQLogger(self.__class__.__name__, self.name)

    def schedule(self, _event: SQEvent, when: int):
        self.logger.debug(f'Schedule Event {_event.name} after {when} sim time')
        _event.scheduled_tick = when + SQTimeBase.get_current_sim_time()
        self.schedule_queue.append(_event)

    def get_event_queue(self, index: int) -> Union[SQEventQueue, None]:
        queue: Union[SQEventQueue, None] = None
        if self.event_queue_list is not None:
            if len(self.event_queue_list) > index:
                queue = self.event_queue_list[index]
            else:
                queue = SQEventQueue()
                self.event_queue_list.append(queue)
        return queue

    def set_schedule_queue(self):
        for _event in self.schedule_queue:
            queue = self.get_event_queue(_event.owner.evt_q)
            if queue is not None:
                queue.schedule(_event=_event)
        self.schedule_queue.clear()

    def run(self):
        self.logger.debug(f'SQEventManager: run')
        self.set_schedule_queue()
        for queue in self.event_queue_list:
            while queue.get_next_event() is not None:
                next_evt = queue.pop_next_event()
                self.logger.debug(f'SQEventManager: Handling Event {next_evt.name}')
                for action in next_evt.actions:
                    action(next_evt)
