from typing import Type, Callable, List
import logging

from abc import ABC, abstractmethod

from pysysq.logging_ctx import SIMLoggingCtx
from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_event_manager import SQEventManager
from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_statistics import SQStatistics, SQStatisticsEntry
from pysysq.sq_base.sq_time_base import SQTimeBase


class SQObject(ABC):
    def __init__(self, name: str, params, event_mgr: SQEventManager, event_q: int = 0, **kwargs):
        self.params = params
        self.name = name
        self.evt_q: int = event_q
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.event_manager = event_mgr
        self.tick: int = 0
        self.self_starting = False
        children = getattr(params, "children")
        self.children = [] if children is None else children
        self.statistics = SQStatistics()
        self.statistics_properties = []

        params_self_ticking = getattr(params, 'is_self_ticking')
        self.is_self_ticking: bool = False if params_self_ticking is None else params_self_ticking
        self.tick_evt = SQEvent(_name=f'{self.name}_tick',
                                owner=self)
        self.start_evt = SQEvent(_name=f'{self.name}_start',
                                 owner=self)
        self.finish_evt = SQEvent(_name=f'{self.name}_finish',
                                  owner=self)
        self.start_evt.actions.append(self.process)

    def __repr__(self):
        return self.name

    def register_property(self, name: str):
        self.statistics_properties.append(name)

    def init(self):
        self.logger.info(f'init')
        for child in self.children:
            assert isinstance(child, SQObject), "all child objects of an SQObject must be derived from SQObject"
            child.init()

    def deinit(self):
        self.logger.info(f'deinit')
        for child in self.children:
            child.deinit()

    def read_statistics(self):
        return self.statistics

    def start(self):
        self.logger.info(f'start')
        if not self.self_starting:
            self.event_manager.schedule(self.start_evt, when=1)
        if self.is_self_ticking:
            self.logger.info(f'is self ticking')
            self.self_connect()
        self.tick = 0
        for child in self.children:
            child.start()

    def finish_indication(self, when=1):
        self.logger.info(f'finish')
        self.event_manager.schedule(self.finish_evt, when=when)

    def self_trigger(self, when=1):
        self.logger.info(f'self_trigger at {self.tick}')
        self.event_manager.schedule(self.tick_evt, when=when)

    def process(self, evt: SQEvent):
        self.logger.info(f'Process Event {evt.owner.name}::{evt.name} on Tick {self.tick}')
        if self.is_self_ticking:
            self.self_trigger()
        for p in self.statistics_properties:
            self.statistics.add(p, getattr(self, p), self.name)

    def connect(self, obj: "SQObject", **kwargs):
        self.finish_evt.add_handler(obj.process)
        return obj

    def self_connect(self):
        self.tick_evt.add_handler(self.process)

    def disconnect(self, obj: "SQObject"):
        self.logger.info(f"disconnecting the observer{obj.name}")
        self.finish_evt.remove_handler(obj.process)

    def get_current_tick(self):
        return self.tick

    def update_tick(self, ticks: int):
        self.tick += ticks
        self.logger.info(f'Updating Current Tick {self.tick}')
