import json
import subprocess
import os
import shutil


class SimulationSetupGenerator:
    def __init__(self, json_file, output='output'):
        with open(json_file, 'r') as file:
            self.data = json.load(file)
        self.helper_factory_code = 'from pysysq import *\n\n'
        self.object_factory_code = 'from pysysq import *\n\n'
        self.code = 'from pysysq import *\n\n'
        self.objects = {}
        self.plot_enabled_objects = []
        self.output_folder = output
        if os.path.exists(self.output_folder):
            shutil.rmtree(self.output_folder)
        os.makedirs(self.output_folder)
        self.object_factories = []
        self.helper_factories = []
        self.created_children = []

    def create_child(self, obj):
        object_name = obj['name']
        if object_name in self.created_children:
            return
        self.created_children.append(object_name)
        is_default_factory = obj['default_factory']

        object_factory = "SQDefaultObjectFactory"
        helper_factory = "SQDefaultHelperFactory"
        if not is_default_factory:
            object_factory = f'{object_name}Factory'
            helper_factory = f'{object_name}HelperFactory'
        self.generate_factory(object_factory, helper_factory)
        plot_enabled = obj['plot']
        child_names = []
        if 'children' in obj:
            children = obj['children']
            child_names = [c['name'] for c in children]
            children.sort(key=lambda x:  (x['type'] != 'SQQueue', x['type'] != 'SQClock'))
            if len(child_names) > 0:
                for child in children:
                    self.create_child(child)
        if plot_enabled:
            self.plot_enabled_objects.append(object_name)
        factory_method = obj['factory_method']
        properties = obj['properties']
        parameters = ""
        for key, value in properties.items():
            if value["type"] != "list":
                parameters += f', {key}={value["value"]}'
            else:
                values = [p for p in value["value"]]
                value_string = ','.join(values)
                parameters += f', {key}=[{value_string}]'

        if len(child_names) > 0:
            child_parms = ','.join(child_names)
            self.code += (
                f'{object_name} = {str.lower(object_factory)}.{factory_method}(name="{object_name}"{parameters}, '
                f'children=[{child_parms}])\n')
        else:
            self.code += f'{object_name} = {str.lower(object_factory)}.{factory_method}(name="{object_name}"{parameters})\n'
        self.objects[object_name] = obj

    def generate_factory(self, object_factory, helper_factory):
        if helper_factory != "SQDefaultHelperFactory" and helper_factory not in self.helper_factories:
            self.helper_factory_code += f'class {helper_factory}(SQDefaultHelperFactory):\n'
            self.helper_factory_code += f'    def __init__(self):\n'
            self.helper_factory_code += f'        super().__init__()\n'
            self.write_helper_factory_file(f'{str.lower(helper_factory)}.py')
            self.code += f'from {str.lower(helper_factory)} import {helper_factory}\n\n'
        if object_factory != "SQDefaultObjectFactory" and object_factory not in self.object_factories:
            self.object_factory_code += f'class {object_factory}(SQDefaultObjectFactory):\n'
            self.object_factory_code += f'    def __init__(self,helper_factory):\n'
            self.object_factory_code += f'        super().__init__(helper_factory=helper_factory)\n'
            self.write_object_factory_file(f'{str.lower(object_factory)}.py')
            self.code += f'from {str.lower(object_factory)} import {object_factory}\n\n'

        if object_factory not in self.object_factories:
            self.code += f'{str.lower(object_factory)} = {object_factory}(helper_factory={helper_factory}())\n\n'
            self.object_factories.append(object_factory)
        if helper_factory not in self.helper_factories:
            self.helper_factories.append(helper_factory)

    def generate_code(self):

        self.create_child(self.data['Simulator'])

        self.code += '\n'
        for object_name, obj in self.objects.items():
            if 'control_flow' in obj:
                if obj['control_flow']:
                    for destination in obj['control_flow']:
                        self.code += f'{object_name}.control_flow({destination})\n'
        for object_name, obj in self.objects.items():
            if 'data_flow' in obj:
                if obj['data_flow']:
                    for data_map in obj['data_flow']:
                        data = data_map['data']
                        destination = data_map['destination']
                        self.code += f'{object_name}.data_flow({destination},{data})\n'

        self.code += '\n'
        simulator_name = self.data['Simulator']['name']
        self.code += f'{simulator_name}.init()\n'
        self.code += f'{simulator_name}.start()\n'

        if len(self.plot_enabled_objects) > 0:
            for object_name in self.plot_enabled_objects:
                self.code += f'{object_name}_Plotter = SQPlotter(name="{object_name}_Plotter", objs=[{object_name}], ' \
                             f'output_file="{object_name}.png", show_plot=False)\n'
                self.code += f'{object_name}_Plotter.plot()\n'
        self.write_simulation_setup_file(f'{str.lower(simulator_name)}.py')

    def write_simulation_setup_file(self, filename):
        actual_file = os.path.join(self.output_folder, filename)
        with open(actual_file, 'w') as file:
            file.write(self.code)

    def write_helper_factory_file(self, filename):
        actual_file = os.path.join(self.output_folder, filename)
        with open(actual_file, 'w') as file:
            file.write(self.helper_factory_code)

    def write_object_factory_file(self, filename):
        actual_file = os.path.join(self.output_folder, filename)
        with open(actual_file, 'w') as file:
            file.write(self.object_factory_code)


def generate(json_file: str, output_folder: str = 'output'):
    generator = SimulationSetupGenerator(json_file=json_file, output=output_folder)
    generator.generate_code()
