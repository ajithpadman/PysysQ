from typing import Type

from abc import ABC, abstractmethod

from pysysq.sq_base.sq_event_manager import SQEventManager


class SQObject(ABC):
    def __init__(self, params, event_mgr: SQEventManager):
        self.params = params
        self.event_manager = event_mgr

    @abstractmethod
    def init(self):
        pass
    @abstractmethod
    def deinit(self):
        pass

    @abstractmethod
    def start(self):
        pass
