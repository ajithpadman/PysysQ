from .sq_filter_helper import SQFilterHelper
from ..sq_packet import SQMetadata


class SQAllPassFilter(SQFilterHelper):

    def __init__(self):
        super().__init__()

    def filter(self, pkt) -> bool:
        metadata = SQMetadata(name='filter_result', owner=self.owner.name, value=True)
        self.owner.data_indication(metadata)
        return True
