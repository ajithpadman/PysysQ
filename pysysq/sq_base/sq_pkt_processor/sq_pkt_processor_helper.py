from abc import ABC, abstractmethod


class SQPktProcessorHelper(ABC):
    @abstractmethod
    def get_processing_ticks(self, pkt):
        pass
