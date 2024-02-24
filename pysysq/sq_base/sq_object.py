from typing import Type, Callable

from abc import ABC, abstractmethod

from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_event_manager import SQEventManager


class SQObject(ABC):
    def __init__(self, params, event_mgr: SQEventManager):
        self.params = params
        self.event_manager = event_mgr
        self.tick: int = 0
        self.evt = SQEvent(_name=f'{self.params.name}_tick',
                           owner=self)

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def deinit(self):
        pass

    @abstractmethod
    def start(self):
        pass

    def schedule(self,when=1):

        self.event_manager.schedule(self.evt, when=when)

    @abstractmethod
    def process(self):
        pass

    def connect(self, obj: "SQObject"):
        self.evt.add_handler(obj.process)
        return obj
