import os

import ruamel_yaml as yaml

script_path = os.path.abspath(__file__)


def read_data_from_file(file_name):
    bms_config_path = os.path.join(
        os.path.dirname(script_path),
        'resources',
        file_name
    )
    print(bms_config_path)
    with open(bms_config_path, 'r') as fp:
        data = yaml.safe_load(fp)
    return data


class BatteryManagementSystem:

    def __init__(self, battery_type, temperature, soc, charge_rate,
                 language='English'):
        self.battery = battery_type
        self.language = language.lower()
        self.values = {'temperature': temperature,
                       'state_of_charge': soc,
                       'charge_rate': charge_rate}
        self.bms_configs = read_data_from_file('configs.yaml')
        self.language_data = read_data_from_file('statements.yaml')
        self._battery_parameters = None

    @staticmethod
    def is_in_range(param_range, value):
        if value < param_range['min'] or value > param_range['max']:
            return False
        return True

    @property
    def battery_parameters(self):
        self._battery_parameters = self.bms_configs['batteries'][self.battery]
        return self._battery_parameters

    def check_battery_limit(self):
        in_limit = 1
        for parameter, value in self.values.items():
            _range = self.battery_parameters[parameter]
            if not self.is_in_range(_range, value):
                print("{} {}".format(
                    parameter,
                    self.language_data['out_of_range'][self.language])
                )
                in_limit = in_limit * 0
        return in_limit

    def is_battery_ok(self):
        if self.check_battery_limit() == 0:
            print(self.language_data['battery_not_ok'][self.language])
        else:
            print(self.language_data['battery_ok'][self.language])


if __name__ == '__main__':
    bms = BatteryManagementSystem('li-ion', 43, 25, 0.9)
    bms.is_battery_ok()
