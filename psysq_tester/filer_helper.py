from pysysq.sq_base.sq_filter import SQFilterHelper
from pysysq.sq_base.sq_packet import SQPacket


class FilterHelper(SQFilterHelper):
    def __init__(self):
        super().__init__()
        self.filter_status = False

    def set_owner(self, owner):
        super().set_owner(owner)
        self.owner.register_property(name='filter_status', owner=self)

    def filter(self, pkt: SQPacket) -> bool:
        if pkt.id % 2 == 0:
            self.filter_status = True
            return True
        else:
            self.filter_status = False
            return False
