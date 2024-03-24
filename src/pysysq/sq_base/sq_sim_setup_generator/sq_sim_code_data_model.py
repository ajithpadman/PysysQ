from typing import List
from dataclasses import dataclass, field
from .sq_sim_data_model import SQSimulatorDataModel


@dataclass
class SQFactoryCodeDataModel:
    name: str
    helper: str


@dataclass
class SQObjectParameter:
    name: str
    value: str

    def __repr__(self):
        return f'{self.name}={self.value}'


@dataclass
class SQDataFlow:
    source: str
    data: str
    destination: str


@dataclass
class SQObjectCodeDataModel:
    name: str
    factory_object_name: str
    factory_method: str
    comment: str
    parameters: str
    imports: List[str] = field(default_factory=list)
    factories: List["SQFactoryCodeDataModel"] = field(default_factory=list)
    queues: List["SQObjectCodeDataModel"] = field(default_factory=list)
    clocks: List["SQObjectCodeDataModel"] = field(default_factory=list)
    sim_objects: List["SQObjectCodeDataModel"] = field(default_factory=list)
    plot_objects: List["SQObjectCodeDataModel"] = field(default_factory=list)
    data_flows: List["SQDataFlow"] = field(default_factory=list)


class SQCodeDataModel:
    def __init__(self, data: SQSimulatorDataModel):
        self._simulators = []
        self._parse(data)

    @property
    def simulators(self):
        return self._simulators

    @staticmethod
    def _remove_duplicates_from_imports(import_list):
        return list(set(import_list))

    @staticmethod
    def _parse_imports(obj):
        import_list = ['from pysysq import *']
        if not obj.is_default_factory:
            factory_name = f'{obj.name}Factory'
            helper_factory = f'{obj.name}HelperFactory'
            import_list.append(f'from {factory_name.lower()} import {factory_name}')
            import_list.append(f'from {helper_factory.lower()} import {helper_factory}')
        return import_list

    @staticmethod
    def _parse_factories(obj):
        factory = None
        if obj.is_default_factory:
            factory = SQFactoryCodeDataModel(name='SQDefaultObjectFactory',
                                             helper='SQDefaultHelperFactory')
        else:
            factory_name = f'{obj.name}Factory'
            helper_name = f'{obj.name}HelperFactory'
            factory = SQFactoryCodeDataModel(name=factory_name,
                                             helper=helper_name)
        return factory

    @staticmethod
    def _format_list_param(list_param: List[str]):
        return "[" + ",".join([f'self.{x.lower()}' for x in list_param]) + "]"

    @staticmethod
    def _parse_parameters(obj):
        sq_params = []
        parameters = {'name': f'"{obj.name}"'}
        if obj.type == 'SQSimulator':
            parameters['max_sim_time'] = obj.max_sim_time
            parameters['time_step'] = obj.time_step
            parameters['children'] = "[" + ",".join([f'self.{x.name.lower()}' for x in obj.children]) + "]"
        elif obj.type == 'SQClock':
            parameters['clk_divider'] = obj.clk_divider
        elif obj.type == 'SQFilter':
            parameters['clk'] = f'self.{obj.clk.lower()}'
            parameters['input_q'] = f'self.{obj.input_q.lower()}'
            parameters['output_q'] = f'self.{obj.output_q.lower()}'
        elif obj.type == 'SQMerger':
            parameters['clk'] = f'self.{obj.clk.lower()}'
            parameters['input_qs'] = "[" + ",".join([f'self.{x.lower()}' for x in obj.input_qs]) + "]"
            parameters['output_q'] = f'self.{obj.output_q.lower()}'
        elif obj.type == 'SQMux':
            parameters['clk'] = f'self.{obj.clk.lower()}'
            parameters['input_qs'] = "[" + ",".join([f'self.{x.lower()}' for x in obj.input_qs]) + "]"
            parameters['output_q'] = f'self.{obj.output_q.lower()}'
        elif obj.type == 'SQDemux':
            parameters['clk'] = f'self.{obj.clk.lower()}'
            parameters['output_qs'] = "[" + ",".join([f'self.{x.lower()}' for x in obj.output_qs]) + "]"
            parameters['input_q'] = f'self.{obj.input_q.lower()}'
        elif obj.type == 'SQPacketGenerator':
            parameters['clk'] = f'self.{obj.clk.lower()}'
            parameters['output_q'] = f'self.{obj.output_q.lower()}'
        elif obj.type == 'SQPktProcessor':
            parameters['clk'] = f'self.{obj.clk.lower()}'
            parameters['input_q'] = f'self.{obj.input_q.lower()}'
            parameters['output_q'] = f'self.{obj.output_q.lower()}'
        elif obj.type == 'SQPktSink':
            parameters['clk'] = f'self.{obj.clk.lower()}'
            parameters['input_q'] = f'self.{obj.input_q.lower()}'
        elif obj.type == 'SQQueue':
            parameters['capacity'] = obj.capacity
        elif obj.type == 'SQSplitter':
            parameters['clk'] = f'self.{obj.clk.lower()}'
            parameters['input_q'] = f'self.{obj.input_q.lower()}'
            parameters['output_qs'] = "[" + ",".join([f'self.{x.lower()}' for x in obj.output_qs]) + "]"
        else:
            parameters = {}
        for key, value in parameters.items():
            param = SQObjectParameter(name=key, value=value)
            sq_params.append(param)

        return sq_params

    def _code_data_model(self, obj):
        factory_name = "SQDefaultObjectFactory"
        if not obj.is_default_factory:
            factory_name = f'{obj.name}Factory'
        import_list = []
        for c in obj.children:
            if len(obj.children) > 0:
                import_list.extend(self._parse_imports(c))
        import_list.extend(self._parse_imports(obj))
        actual_imports = self._remove_duplicates_from_imports(import_list)
        factories = [self._parse_factories(c) for c in obj.children
                     if len(obj.children) > 0]
        actual_factories = self._remove_duplicate_factories(factories)
        parameters_list = ','.join([x.__repr__() for x in self._parse_parameters(obj)])
        data_flows = self._parse_data_flows(obj)
        return SQObjectCodeDataModel(name=obj.name,
                                     factory_object_name=f'self.{factory_name.lower()}',
                                     factory_method=obj.factory_method,
                                     comment=obj.comment,
                                     parameters=parameters_list,
                                     factories=actual_factories,
                                     queues=[self._parse_queue(c) for c in obj.children
                                             if len(obj.children) > 0 and c.type == 'SQQueue'],
                                     clocks=[self._parse_clock(c) for c in obj.children
                                             if len(obj.children) > 0 and c.type == 'SQClock'],
                                     sim_objects=[self._parse_other_sim_object(c) for c in obj.children
                                                  if len(obj.children) > 0 and
                                                  c.type != 'SQClock' and
                                                  c.type != 'SQQueue' and
                                                  c.type != 'SQSimulator'],
                                     plot_objects=[x.name for x in obj.children if x.plot],
                                     data_flows=data_flows,
                                     imports=actual_imports
                                     )

    def _parse_queue(self, obj):
        queue = None
        if obj.type == 'SQQueue':
            queue = self._code_data_model(obj)
        return queue

    def _parse_clock(self, obj):
        clock = None
        if obj.type == 'SQClock':
            clock = self._code_data_model(obj)
        return clock

    def _parse_other_sim_object(self, obj):
        sim_object = None
        if obj.type != 'SQQueue' and obj.type != 'SQClock' and obj.type != 'SQSimulator':
            sim_object = self._code_data_model(obj)
        return sim_object

    def _parse_simulators(self, obj):
        if obj.type == 'SQSimulator':
            self.simulators.append(self._code_data_model(obj))

    @staticmethod
    def _parse_data_flows(obj):
        dataflows = []

        for data_flow in obj.data_flows:
            dataflows.append(SQDataFlow(source=f'self.{obj.name.lower()}', data=data_flow.data,
                                        destination=f'self.{data_flow.destination.lower()}'))
        for ch in obj.children:
            dataflows.extend(SQCodeDataModel._parse_data_flows(ch))
        return dataflows

    @staticmethod
    def _remove_duplicate_factories(factories):
        unique_factories = {}
        for factory in factories:
            if factory.name not in unique_factories:
                unique_factories[factory.name] = factory
        return list(unique_factories.values())

    def _parse(self, data: SQSimulatorDataModel):
        self._parse_simulators(data)
