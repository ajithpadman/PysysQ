import matplotlib.pyplot as plt

from pysysq.sq_base.sq_logger import SQLogger


class SQPlotter:
    def __init__(self, name: str, objs: []):
        self.name = name
        self.objs = objs
        self.logger = SQLogger(self.__class__.__name__,self.name)

    def plot(self):
        plt.figure()
        for obj in self.objs:
            self.logger.debug(f'Plotting {obj.name}')
            properties = obj.read_statistics().get_all_property_names(obj.name)
            for property_name in properties:
                self.plot_property(property_name=property_name, obj=obj)
        plt.legend()
        plt.xlabel('Simulation Time')
        plt.ylabel('Property Value')
        plt.title(f'SQObject Properties')
        plt.savefig(f'Statistics.png')
        plt.show()

    def plot_property(self, property_name: str, obj):
        self.logger.debug(f'Plotting {obj.name} [{property_name}]')
        property_values = obj.read_statistics().get_property(name=property_name, owner=obj.name)
        x_values = [entry.sim_time for entry in property_values]
        y_values = [entry.value for entry in property_values]
        plt.plot(x_values, y_values, label=f'{obj.name}[{property_name}]')
