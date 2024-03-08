from pysysq.sq_base.sq_filter.sq_pass_all_filter import SQAllPassFilter
from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_queue import SQQueue


class SQFilter(SQObject):
    def __init__(self, name: str, event_mgr, **kwargs):
        super().__init__(name, event_mgr, **kwargs)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.filter_config = kwargs.get('filter_config', SQAllPassFilter())

    def process(self, evt):
        super().process(evt)
        if evt.owner is not self:

            if self.filter_config.filter(evt.data):
                self.finish_indication(data=evt.data)
        else:
            if evt.name != f'{self.name}_start':
                self.logger.error(f'Ignoring Self Event {evt}')
