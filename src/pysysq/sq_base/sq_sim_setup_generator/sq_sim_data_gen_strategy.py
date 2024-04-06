from abc import ABC, abstractmethod
from .sq_sim_data_model import (SQSimDataModel, DataFlow)


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
        data = dict(
            name=data['name'],
            clk_divider=data['clk_divider']
        )
        clk_model = SQSimDataModel(
            name=data['name'],
            type=data['type'],
            comment=data['description'],
            data_flows=self.get_data_flows(data),
            plot=data['plot'],
            sq_object_data=data,
            children=[],
        )
        return clk_model


class SQSimulatorDataGenStrategy(SQSimDataGenStrategy):
    def __init__(self, ctx):
        super().__init__(ctx)

    def generate(self, data: dict) -> SQSimDataModel:
        children = [self.context.generate(x) for x in data['children']]
        children_names = [f'self.{str(x.sq_object_data["name"]).lower()}' for x in children]
        data = dict(
            name=data['name'],
            max_sim_time=data['max_sim_time'],
            time_step=data['time_step'],
            children=children_names,
            helper="default"
        )
        return SQSimDataModel(
            name=data['name'],
            type=data['type'],
            comment=data['description'],
            data_flows=self.get_data_flows(data),
            plot=data['plot'],
            sq_object_data=data,
            children=children,
        )


class SQSISODataGenStrategy(SQSimDataGenStrategy):
    def __init__(self, ctx):
        super().__init__(ctx)

    def generate(self, data: dict) -> SQSimDataModel:
        data = dict(
            name=data['name'],
            clk=data['clk'],
            input_q=data['input_q'],
            output_q=data['output_q']
        )
        return SQSimDataModel(
            name=data['name'],
            type=data['type'],
            comment=data['description'],
            data_flows=self.get_data_flows(data),
            plot=data['plot'],
            sq_object_data=data,
            children=[],
        )


class SQSIMODataGenStrategy(SQSimDataGenStrategy):
    def __init__(self, ctx):
        super().__init__(ctx)

    def generate(self, data: dict) -> SQSimDataModel:
        data = dict(
            name=data['name'],
            clk=data['clk'],
            input_qs=data['input_q'],
            output_q=data['output_qs']
        )
        return SQSimDataModel(
            name=data['name'],
            type=data['type'],
            comment=data['description'],
            data_flows=self.get_data_flows(data),
            plot=data['plot'],
            sq_object_data=data,
            children=[],
        )


class SQMISODataGenStrategy(SQSimDataGenStrategy):
    def __init__(self, ctx):
        super().__init__(ctx)

    def generate(self, data: dict) -> SQSimDataModel:
        data = dict(
            name=data['name'],
            clk=data['clk'],
            input_qs=data['input_qs'],
            output_q=data['output_q']
        )
        return SQSimDataModel(
            name=data['name'],
            type=data['type'],
            comment=data['description'],
            data_flows=self.get_data_flows(data),
            plot=data['plot'],
            sq_object_data=data,
            children=[],
        )


class SQSINODataGenStrategy(SQSimDataGenStrategy):
    def __init__(self, ctx):
        super().__init__(ctx)

    def generate(self, data: dict) -> SQSimDataModel:
        data = dict(
            name=data['name'],
            clk=data['clk'],
            input_q=data['input_q']
        )
        return SQSimDataModel(
            name=data['name'],
            type=data['type'],
            comment=data['description'],
            data_flows=self.get_data_flows(data),
            plot=data['plot'],
            sq_object_data=data,
            children=[],

        )


class SQNISODataGenStrategy(SQSimDataGenStrategy):
    def __init__(self, ctx):
        super().__init__(ctx)

    def generate(self, data: dict) -> SQSimDataModel:
        data = dict(
            name=data['name'],
            clk=data['clk'],
            output_q=data['output_q']
        )
        return SQSimDataModel(
            name=data['name'],
            type=data['type'],
            comment=data['description'],
            data_flows=self.get_data_flows(data),
            plot=data['plot'],
            sq_object_data=data,
            children=[],
        )


class SQQueueDataGenStrategy(SQSimDataGenStrategy):
    def __init__(self, ctx):
        super().__init__(ctx)

    def generate(self, data: dict) -> SQSimDataModel:
        data = dict(
            name=data['name'],
            capacity=data['capacity'],
        )
        qs = SQSimDataModel(
            name=data['name'],
            type=data['type'],
            comment=data['description'],
            data_flows=self.get_data_flows(data),
            children=[],
            plot=data['plot'],
            sq_object_data=data,
        )
        return qs
