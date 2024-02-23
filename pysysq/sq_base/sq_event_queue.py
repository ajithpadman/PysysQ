from typing import List, Union

from pysysq.sq_base.sq_event import SQEvent


class SQEventQueue:
    def __init__(self):
        self.queue: List[SQEvent] = []

    def schedule(self, _event: SQEvent):
        self.queue.append(_event)

    def pop_next_event(self) -> Union[SQEvent, None]:
        if len(self.queue) > 0:
            evt = min(self.queue, key=lambda x: x.scheduled_tick)
            self.queue.remove(evt)
            return evt
        else:
            return None

    def get_next_event(self):
        if len(self.queue) > 0:
            return min(self.queue, key=lambda x: x.scheduled_tick)
        else:
            return None
