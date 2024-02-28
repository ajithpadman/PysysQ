from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_event_manager import SQEventManager
from pysysq.sq_base.sq_object import SQObject


class SQPacketGenerator(SQObject):
    def __init__(self, name: str, params, event_mgr: SQEventManager):
        super().__init__(name, params, event_mgr)

    def process(self, evt: SQEvent):
        super().process(evt)
        self.finish_evt.data = self.params.generate()
        self.finish_indication()
