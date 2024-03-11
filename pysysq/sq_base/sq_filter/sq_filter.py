from pysysq.sq_base.sq_filter import SQFilterHelper
from pysysq.sq_base.sq_filter.sq_pass_all_filter import SQAllPassFilter
from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_queue import SQQueue


class SQFilter(SQObject):
    def __init__(self, name: str, event_mgr, helper: SQFilterHelper, **kwargs):
        super().__init__(name, event_mgr, **kwargs)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.filter_config = helper

    def process_packet(self, evt):
        super().process_packet(evt)
        if evt.owner is not self:

            if self.filter_config.filter(evt.data):
                self.finish_indication(data=evt.data)
        else:
            if evt.name != f'{self.name}_start':
                self.logger.error(f'Ignoring Self Event {evt}')
