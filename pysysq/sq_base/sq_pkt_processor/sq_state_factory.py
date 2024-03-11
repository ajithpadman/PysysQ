from typing import Union

from pysysq.sq_base.sq_pkt_processor.sq_pkt_proc_complete import SQPktProcStateComplete
from pysysq.sq_base.sq_pkt_processor.sq_pkt_proc_idle import SQPktProcStateIdle
from pysysq.sq_base.sq_pkt_processor.sq_pkt_proc_processing import SQPktProcStateProcessing
from pysysq.sq_base.sq_pkt_processor.sq_pkt_processor_state import SQPktProcState


class SQStateFactory:

    def create_state(self, name: str, owner) -> Union[SQPktProcState,None]:
        state = None
        if name == "IDLE":
            state = SQPktProcStateIdle(owner=owner, factory=self)
        elif name == "PROCESSING":
            state =  SQPktProcStateProcessing(owner=owner, factory=self)
        elif name == "COMPLETE":
            state = SQPktProcStateComplete(owner=owner, factory=self)
        else:
            state = None
        return state

