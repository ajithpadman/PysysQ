from abc import ABC

from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_event.sq_event import EventType
from pysysq.sq_base.sq_event.sq_event_manager import SQEventManager
from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_packet.sq_metadata import SQMetadata
from pysysq.sq_base.sq_statistics import SQStatistics


class SQObject(ABC):
    """
    Base class for all objects in the simulation
    """

    def __init__(self, name: str, event_mgr: SQEventManager, **kwargs):
        """
        Constructor for the SQObject
        :param name: Name of the Object
        :param event_mgr: Event Manager to be used
        :param kwargs: A dictionary of optional parameters
            event_q: Event Queue to be used
            children: List of children objects
            is_self_ticking: Boolean to indicate if the object is self ticking
        """
        self.name = name
        self.evt_q: int = kwargs.get('event_q', 0)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.event_manager = event_mgr
        self.tick: int = 0
        self.self_starting = False
        self.children = kwargs.get('children', [])
        self.statistics = SQStatistics()
        self.statistics_properties = []
        self.metadata = kwargs.get('metadata', {})
        self.is_self_ticking: bool = kwargs.get('is_self_ticking', False)
        self.data_flow_map = kwargs.get('data_flow_map', {})
        self.tick_evt = SQEvent(_name=f'{self.name}_tick',
                                owner=self)
        self.tick_evt.type = EventType.TICK_EVENT

        self.start_evt = SQEvent(_name=f'{self.name}_start',
                                 owner=self)
        self.start_evt.type = EventType.START_EVT
        self.start_evt.add_handler(self.process)
        self.finish_evt = SQEvent(_name=f'{self.name}_finish',
                                  owner=self)
        self.finish_evt.type = EventType.PROCESS_EVT

        self.metadata_evt = SQEvent(_name=f'{self.name}_metadata',
                                    owner=self)

        self.metadata_evt.type = EventType.METADATA_EVT

    def __repr__(self):
        return self.name

    def set_log_level(self, level):
        self.logger.set_level(level)

    def register_property(self, name: str):
        self.statistics_properties.append(name)

    def process_metadata(self, evt: SQEvent):
        if evt.type == EventType.METADATA_EVT:
            if evt.data is not None:
                if isinstance(evt.data, SQMetadata):
                    if evt.data.name in self.data_flow_map:
                        my_attr = self.data_flow_map[evt.data.name]
                        if my_attr in self.metadata:
                            self.metadata[my_attr] = evt.data
                        else:
                            self.logger.error(f"Mapping for Metadata {evt.data.name}  found in {self.name} "
                                              f"object but not registered as a metadata attribute")
                    else:
                        self.logger.warning(f"Mapping for Metadata {evt.data.name} not found in {self.name} object")

                else:
                    self.logger.error(f"Metadata {evt.data} not a SQMetadata object")
        else:
            self.logger.error(f"Ignoring Metadata Event {evt.name} from {evt.owner.name}")

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

    def finish_indication(self, data=None, when=1):
        self.logger.info(f'finish indication')
        self.finish_evt.data = data
        self.event_manager.schedule(self.finish_evt, when=when)

    def data_indication(self, data: SQMetadata, when=1):
        self.logger.info(f'data indication')
        self.metadata_evt.data = data
        self.event_manager.schedule(self.metadata_evt, when=when)

    def self_trigger(self, when=1):
        self.logger.info(f'self_trigger at {self.tick}')
        self.event_manager.schedule(self.tick_evt, when=when)

    def collect_statistics(self):
        for p in self.statistics_properties:
            self.statistics.add(p, getattr(self, p), self.name)

    def process(self, evt: SQEvent):
        self.logger.info(f'Process Event {evt.owner.name}::{evt.name} on Tick {self.tick}')
        if self.is_self_ticking:
            self.self_trigger()
        self.collect_statistics()

    def control_flow(self, obj: "SQObject", **kwargs):
        self.finish_evt.add_handler(obj.process)
        return obj

    def data_flow(self, obj: "SQObject"):
        self.metadata_evt.add_handler(obj.process_metadata)
        return obj

    def self_connect(self):
        self.tick_evt.add_handler(self.process)

    def disconnect_control_flow(self, obj: "SQObject"):
        self.logger.info(f"disconnecting the observer{obj.name} from control flow")
        self.finish_evt.remove_handler(obj.process)

    def disconnect_data_flow(self, obj: "SQObject"):
        self.logger.info(f"disconnecting the observer{obj.name} from dataflow")
        self.metadata_evt.remove_handler(obj.process_metadata)

    def get_current_tick(self):
        return self.tick

    def update_tick(self, ticks: int):
        self.tick += ticks
        self.logger.info(f'Updating Current Tick {self.tick}')
