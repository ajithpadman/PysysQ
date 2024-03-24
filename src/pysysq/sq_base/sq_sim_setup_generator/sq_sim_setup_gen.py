import json
import os
import shutil

from .sq_sim_data_gen_ctx import SQSimDataGenCtx
from .sq_sim_code_data_model import SQCodeDataModel
from jinja2 import FileSystemLoader, Environment

_default_json_file = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config'), "input.json")


class SQSimSetupGen:
    def __init__(self, json_file: str = _default_json_file):
        with open(json_file, 'r') as file:
            self.data = json.load(file)
        self.gen_ctx = SQSimDataGenCtx()
        self.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
        file_loader = FileSystemLoader(self.template_folder)
        self.env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)

    def generate(self, output_folder: str):
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
        os.makedirs(output_folder)
        data = self.gen_ctx.generate(self.data['Simulator'])
        code_data_model = SQCodeDataModel(data)
        template = self.env.get_template('sim_setup.py.j2')
        obj_factory_template = self.env.get_template('obj_factory.py.j2')
        hlpr_factory_template = self.env.get_template('helper_factory.py.j2')
        for sim in code_data_model.simulators:
            output = template.render(model=sim)
            self.create_file(data=output, output_folder=output_folder, file=f'{sim.name.lower()}_setup.py')
            for factory in sim.factories:
                if factory.name != 'SQDefaultObjectFactory':
                    print(factory.name)
                    output = obj_factory_template.render(model=factory)
                    self.create_file(data=output, output_folder=output_folder, file=f'{factory.name.lower()}.py')
                    output = hlpr_factory_template.render(model=factory)
                    self.create_file(data=output, output_folder=output_folder, file=f'{factory.helper.lower()}.py')
        print("Done")

    @staticmethod
    def create_file(data, output_folder, file):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        file_name = os.path.join(output_folder, file)
        f = open(file_name, "w")
        f.write(data)
        f.write('\n')
        f.close()
