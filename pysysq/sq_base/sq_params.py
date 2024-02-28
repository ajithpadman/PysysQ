from dataclasses import dataclass


@dataclass
class SQParams:
    def __getattr__(self, item):
        return None


