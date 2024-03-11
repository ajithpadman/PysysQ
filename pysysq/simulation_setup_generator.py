import json
import subprocess


class SimulationSetupGenerator:
    def __init__(self, json_file, show_plot=False):
        with open(json_file, 'r') as file:
            self.data = json.load(file)
        self.code = 'from pysysq import *\n\n'
        self.objects = {}
        self.plot_enabled_objects = []
        self.show_plot = show_plot

    def generate_code(self):
        self.code += 'factory = SQDefaultObjectFactory(helper_factory=SQDefaultHelperFactory())\n\n'
        for obj in self.data['Simulator']['children']:
            class_name = obj['type']
            object_name = obj['name']
            plot_enabled = obj['plot']
            if plot_enabled:
                self.plot_enabled_objects.append(object_name)
            factory_method = obj['factory_method']
            properties = obj['properties']
            parameters = ""
            for key, value in properties.items():
                parameters += f', {key}={value["value"]}'

            self.code += f'{object_name} = factory.{factory_method}(name="{object_name}"{parameters})\n'
            self.objects[object_name] = obj
        self.code += '\n'
        for object_name, obj in self.objects.items():
            if obj['control_flow']:
                for destination in obj['control_flow']:
                    self.code += f'{object_name}.control_flow({destination})\n'

        self.code += '\n'
        simulator_name = self.data['Simulator']['name']
        sim_properties = self.data['Simulator']['properties']
        sim_factory = self.data['Simulator']['factory_method']
        sim_parameters = ""
        for key, value in sim_properties.items():
            sim_parameters += f', {key}={value["value"]}'
        sim_children = [name for name, _ in self.objects.items()]
        sim_children = ', '.join(sim_children)

        self.code += (f'{simulator_name} = factory.{sim_factory}(name="{simulator_name}"{sim_parameters}, '
                      f'children=[{sim_children}])\n')
        self.code += f'{simulator_name}.init()\n'
        self.code += f'{simulator_name}.start()\n'
        if len(self.plot_enabled_objects) > 0:
            for object_name in self.plot_enabled_objects:
                self.code += f'sq_plotter = SQPlotter(name="{object_name}_Plotter", objs=[{object_name}], ' \
                             f'output_file="{object_name}.png", show_plot={self.show_plot})\n'
                self.code += f'sq_plotter.plot()\n'

    def write_to_file(self, filename):
        with open(filename, 'w') as file:
            file.write(self.code)

    def run_file(self, filename):
        subprocess.run(['python3', filename])


def generate_and_run(json_file: str, simulation: str, show_plot: bool = False):
    generator = SimulationSetupGenerator(json_file=json_file, show_plot=show_plot)
    generator.generate_code()
    generator.write_to_file(f'{simulation}.py')
    generator.run_file(f'{simulation}.py')

