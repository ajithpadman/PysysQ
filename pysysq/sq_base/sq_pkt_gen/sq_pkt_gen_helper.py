from abc import ABC, abstractmethod


class SQPktGenHelper(ABC):
    @abstractmethod
    def generate_pkts(self):
        pass
