import logging

from pysysq.sq_base.sq_time_base import SQTimeBase


class SIMLoggingCtx(logging.Filter):
    def filter(self, record):
        record.sim_time = SQTimeBase.get_current_sim_time()
        return True
