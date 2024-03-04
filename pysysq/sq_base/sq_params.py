from dataclasses import dataclass


@dataclass
class SQParams:
    parameters: dict = None

    def __getattr__(self, item):
        return None
