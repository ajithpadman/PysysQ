import copy
from typing import List

from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_port_selection import PortSelection
from pysysq.sq_base.sq_queue import SQQueue


class SQReplicator(SQObject):
    def __init__(self, name: str, params, event_mgr):
        super().__init__(name, params, event_mgr)
        self.logger = SQLogger(self.__class__.__name__,self.name)
        self.no_of_ports = params.no_of_ports
        self.queues: List[SQQueue] = []
        self.current_queue = 0
        for p in range(self.no_of_ports):
            self.queues.append(SQQueue(f'{self.name}_Q{p}', params, event_mgr))


    def process(self, evt):
        super().process(evt)

        if self.params.port_selection == PortSelection.DYNAMIC:
            self.current_queue = self.params.get_selected_queue(evt)
            self.logger.info(f'Selected Queue through dynamic port selection  {self.current_queue}')
            self.queues[self.current_queue].process(copy.copy(evt))
        elif self.params.port_selection == PortSelection.ROUND_ROBIN:
            self.current_queue = (self.current_queue + 1) % self.no_of_ports
            self.queues[self.current_queue].process(copy.copy(evt))
            self.logger.info(f' Selected Queue through Round Robin port selection  {self.current_queue}')
        elif self.params.port_selection == PortSelection.BROADCAST:
            self.logger.info(f' Broadcasting to all queues')
            for q in self.queues:
                q.process(copy.copy(evt))

    def get_queue(self, index):
        return self.queues[index]
