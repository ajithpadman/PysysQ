from abc import ABC, abstractmethod
from .sq_sim_data_model import (SQSimDataModel,
                                SQClockDataModel,
                                SQSimulatorDataModel,
                                SQSISODataModel, SQSIMODataModel,
                                SQMISODataModel,
                                SQSINODataModel,
                                SQNISODataModel,
                                SQQueueDataModel,DataFlow)


class SQSimDataGenStrategy(ABC):
    def __init__(self, context):
        self.context = context

    @abstractmethod
    def generate(self, data: dict) -> SQSimDataModel:
        pass

    def get_data_flows(self, data: dict):
        data_flows = []
        if 'data_flow' not in data:
            return data_flows
        for d in data['data_flow']:
            data_flows.append(DataFlow(data=d['data'], destination=d['destination']))
        return data_flows


class SQClockDataGenStrategy(SQSimDataGenStrategy):
    def __init__(self, ctx):
        super().__init__(ctx)

    def generate(self, data: dict) -> SQSimDataModel:
        clk_model = SQClockDataModel(name=data['name'],
                                     type=data['type'],
                                     is_default_factory=data['default_factory'],
                                     factory_method=self.context.factory,
                                     comment=data['description'],
                                     clk_divider=data['clk_divider'],
                                     data_flows=self.get_data_flows(data),
                                     children=[],
                                     plot=data['plot']
                                     )
        return clk_model


class SQSimulatorDataGenStrategy(SQSimDataGenStrategy):
    def __init__(self, ctx):
        super().__init__(ctx)

    def generate(self, data: dict) -> SQSimDataModel:
        return SQSimulatorDataModel(name=data['name'],
                                    type=data['type'],
                                    factory_method=self.context.factory,
                                    is_default_factory=data['default_factory'],
                                    comment=data['description'],
                                    data_flows=self.get_data_flows(data),
                                    max_sim_time=data['max_sim_time'],
                                    time_step=data['time_step'],
                                    children=[self.context.generate(x) for x in data['children']],
                                    plot=data['plot']
                                    )


class SQSISODataGenStrategy(SQSimDataGenStrategy):
    def __init__(self, ctx):
        super().__init__(ctx)

    def generate(self, data: dict) -> SQSimDataModel:
        return SQSISODataModel(name=data['name'],
                               type=data['type'],
                               factory_method=self.context.factory,
                               is_default_factory=data['default_factory'],
                               comment=data['description'],
                               data_flows=self.get_data_flows(data),
                               clk=data['clk'],
                               input_q=data['input_q'],
                               output_q=data['output_q'],
                               children=[],
                               plot=data['plot']
                               )


class SQSIMODataGenStrategy(SQSimDataGenStrategy):
    def __init__(self, ctx):
        super().__init__(ctx)

    def generate(self, data: dict) -> SQSimDataModel:
        return SQSIMODataModel(name=data['name'],
                               type=data['type'],
                               factory_method=self.context.factory,
                               is_default_factory=data['default_factory'],
                               comment=data['description'],
                               data_flows=self.get_data_flows(data),
                               clk=data['clk'],
                               input_q=data['input_q'],
                               output_qs=data['output_qs'],
                               children=[],
                               plot=data['plot']
                               )


class SQMISODataGenStrategy(SQSimDataGenStrategy):
    def __init__(self, ctx):
        super().__init__(ctx)

    def generate(self, data: dict) -> SQSimDataModel:
        return SQMISODataModel(name=data['name'],
                               type=data['type'],
                               factory_method=self.context.factory,
                               is_default_factory=data['default_factory'],
                               comment=data['description'],
                               data_flows=self.get_data_flows(data),
                               clk=data['clk'],
                               input_qs=data['input_qs'],
                               output_q=data['output_q'],
                               children=[],
                               plot=data['plot']
                               )


class SQSINODataGenStrategy(SQSimDataGenStrategy):
    def __init__(self, ctx):
        super().__init__(ctx)

    def generate(self, data: dict) -> SQSimDataModel:
        return SQSINODataModel(name=data['name'],
                               type=data['type'],
                               factory_method=self.context.factory,
                               is_default_factory=data['default_factory'],
                               comment=data['description'],
                               data_flows=self.get_data_flows(data),
                               clk=data['clk'],
                               input_q=data['input_q'],
                               children=[],
                               plot=data['plot']
                               )


class SQNISODataGenStrategy(SQSimDataGenStrategy):
    def __init__(self, ctx):
        super().__init__(ctx)

    def generate(self, data: dict) -> SQSimDataModel:
        return SQNISODataModel(name=data['name'],
                               type=data['type'],
                               factory_method=self.context.factory,
                               is_default_factory=data['default_factory'],
                               comment=data['description'],
                               data_flows=self.get_data_flows(data),
                               clk=data['clk'],
                               output_q=data['output_q'],
                               children=[],
                               plot=data['plot']
                               )


class SQQueueDataGenStrategy(SQSimDataGenStrategy):
    def __init__(self, ctx):
        super().__init__(ctx)

    def generate(self, data: dict) -> SQSimDataModel:
        qs = SQQueueDataModel(name=data['name'],
                              type=data['type'],
                              factory_method=self.context.factory,
                              is_default_factory=data['default_factory'],
                              comment=data['description'],
                              data_flows=self.get_data_flows(data),
                              capacity=data['capacity'],
                              children=[],
                              plot=data['plot']
                              )
        return qs
