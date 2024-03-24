from abc import ABC, abstractmethod


class SQPktGenHelper(ABC):

    def __init__(self):
        self.owner = None

    @abstractmethod
    def generate_pkts(self):
        pass

    @abstractmethod
    def set_params(self, **kwargs):
        pass

    def set_owner(self, owner):
        self.owner = owner
