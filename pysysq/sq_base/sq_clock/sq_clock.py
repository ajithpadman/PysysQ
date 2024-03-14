from pysysq.sq_base.sq_event import SQEvent
from pysysq.sq_base.sq_event.sq_event_manager import SQEventManager
from pysysq.sq_base.sq_logger import SQLogger
from pysysq.sq_base.sq_object import SQObject
from pysysq.sq_base.sq_time_base import SQTimeBase


class SQClock(SQObject):
    """
    A Clock object that ticks at a given frequency based on the clk_divider
    """

    def __init__(self, name: str, event_mgr: SQEventManager, clk_divider: int, **kwargs):
        """
         Constructor for SQClock
        :param name:
        :param event_mgr: Event Manager to be used
        :param clk_divider: Clock Divider value
        :param kwargs: optional parameters
            evt_q: Event Queue index
        """
        super().__init__(name, event_mgr, **kwargs)
        self.logger = SQLogger(self.__class__.__name__, self.name)
        self.clk_divider = clk_divider
        self.is_self_ticking = True

    def process_packet(self, evt: SQEvent):
        current_sim_time = SQTimeBase.get_current_sim_time()
        # only tick if the current sim time is a multiple of clk_divider
        if current_sim_time % self.clk_divider == 0:
            self.tick += 1
            self.logger.info(
                f" Clock Tick = {self.tick} on sim time {current_sim_time}")
            self.finish_indication()
        else:
            self.logger.debug(
                f" Skipping at Clock Tick = {self.tick} on sim time {current_sim_time}")
        super().process_packet(evt)
