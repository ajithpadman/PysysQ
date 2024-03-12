import json
import subprocess


class SimulationSetupGenerator:
    def __init__(self, json_file, show_plot=False):
        with open(json_file, 'r') as file:
            self.data = json.load(file)
        self.helper_factory_code = 'from pysysq import *\n\n'
        self.object_factory_code = 'from pysysq import *\n\n'
        self.code = 'from pysysq import *\n\n'
        self.objects = {}
        self.plot_enabled_objects = []
        self.show_plot = show_plot

    def create_child(self, obj):
        class_name = obj['type']
        object_name = obj['name']
        plot_enabled = obj['plot']
        children = obj['children']
        child_names = [c['name'] for c in children]
        if len(child_names) > 0:
            for child in children:
                self.create_child(child)
        if plot_enabled:
            self.plot_enabled_objects.append(object_name)
        factory_method = obj['factory_method']
        properties = obj['properties']
        parameters = ""
        for key, value in properties.items():
            parameters += f', {key}={value["value"]}'
        if len(child_names) > 0:
            child_parms = ','.join(child_names)
            self.code += f'{object_name} = factory.{factory_method}(name="{object_name}"{parameters} ,children=[{child_parms}])\n'
        else:
            self.code += f'{object_name} = factory.{factory_method}(name="{object_name}"{parameters})\n'
        self.objects[object_name] = obj

    def generate_factory(self, object_factory, helper_factory):
        if helper_factory != "SQDefaultHelperFactory":
            self.helper_factory_code += f'class {helper_factory}(SQDefaultHelperFactory):\n'
            self.helper_factory_code += f'    def __init__(self):\n'
            self.helper_factory_code += f'        super().__init__()\n'
            self.write_helper_factory_file(f'{str.lower(helper_factory)}.py')
            self.code += f'from {str.lower(helper_factory)} import {helper_factory}\n\n'
        if object_factory != "SQDefaultObjectFactory":
            self.object_factory_code += f'class {object_factory}(SQDefaultObjectFactory):\n'
            self.object_factory_code += f'    def __init__(self,helper_factory):\n'
            self.object_factory_code += f'        super().__init__(helper_factory=helper_factory)\n'
            self.write_object_factory_file(f'{str.lower(object_factory)}.py')
            self.code += f'from {str.lower(object_factory)} import {object_factory}\n\n'

        self.code += f'factory = {object_factory}(helper_factory={helper_factory}())\n\n'

    def generate_code(self):
        object_factory = self.data['Simulator']['factory']
        helper_factory = self.data['Simulator']['helper_factory']

        self.generate_factory(object_factory, helper_factory)
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
                self.code += f'sq_plotter = SQPlotter(name="{object_name}_Plotter", objs=[{object_name}], ' \
                             f'output_file="{object_name}.png", show_plot={self.show_plot})\n'
                self.code += f'sq_plotter.plot()\n'

    def write_simulation_setup_file(self, filename):
        with open(filename, 'w') as file:
            file.write(self.code)

    def write_helper_factory_file(self, filename):
        with open(filename, 'w') as file:
            file.write(self.helper_factory_code)

    def write_object_factory_file(self, filename):
        with open(filename, 'w') as file:
            file.write(self.object_factory_code)

    def run_file(self, filename):
        subprocess.run(['python3', filename])


def generate_and_run(json_file: str, simulation: str, show_plot: bool = False):
    generator = SimulationSetupGenerator(json_file=json_file, show_plot=show_plot)
    generator.generate_code()
    generator.write_simulation_setup_file(f'{simulation}.py')
    generator.run_file(f'{simulation}.py')
