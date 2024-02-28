from dataclasses import dataclass

from pysysq.sq_base.sq_object_params import SQObjectParams


@dataclass
class SQClockParams(SQObjectParams):
    clk_time_steps: int = 1

    def __getattr__(self, item):
        if item == 'clk_time_steps':
            return 1
        else:
            return None
