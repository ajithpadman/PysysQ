from dataclasses import dataclass
from typing import List


@dataclass
class DataFlow:
    data: str
    destination: str


@dataclass
class SQSimDataModel:
    name: str
    type: str
    is_default_factory: bool
    factory_method: str
    comment: str
    data_flows: List[DataFlow]


@dataclass
class SQObjectDataModel(SQSimDataModel):
    children: List[SQSimDataModel]
    plot: bool


@dataclass
class SQSimulatorDataModel(SQObjectDataModel):
    max_sim_time: int
    time_step: float


@dataclass
class SQClockDataModel(SQObjectDataModel):
    clk_divider: int


@dataclass
class SQClockedObjectDataModel(SQObjectDataModel):
    clk: str


@dataclass
class SQSISODataModel(SQClockedObjectDataModel):
    input_q: str
    output_q: str


@dataclass
class SQMISODataModel(SQClockedObjectDataModel):
    input_qs: List[str]
    output_q: str


@dataclass
class SQSIMODataModel(SQClockedObjectDataModel):
    output_qs: List[str]
    input_q: str


@dataclass
class SQNISODataModel(SQClockedObjectDataModel):
    output_q: str


@dataclass
class SQSINODataModel(SQClockedObjectDataModel):
    input_q: str


@dataclass
class SQQueueDataModel(SQObjectDataModel):
    capacity: int
