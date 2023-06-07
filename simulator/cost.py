import configparser
from simulator.time import Timer
import os


class SimpleCost:
    _config = configparser.ConfigParser()
    _config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    _config.read(_config_file)

    # rate per hour
    _on_peak_ec_rate = float(_config.get('Cost', 'on_peak_ec_rate'))
    _off_peak_ec_rate = float(_config.get('Cost', 'off_peak_ec_rate'))
    _on_peak_dc_rate = float(_config.get('Cost', 'on_peak_dc_rate'))
    _off_peak_dc_rate = float(_config.get('Cost', 'off_peak_dc_rate'))

    @staticmethod
    def get_on_peak_ec_rate():
        return SimpleCost._on_peak_ec_rate

    @staticmethod
    def get_off_peak_ec_rate():
        return SimpleCost._off_peak_ec_rate

    @staticmethod
    def get_on_peak_dc_rate():
        return SimpleCost._on_peak_dc_rate

    @staticmethod
    def get_off_peak_dc_rate():
        return SimpleCost._off_peak_dc_rate

#For test
if __name__=='__main__':
    print("Energy charge rate on peak: ", SimpleCost.get_on_peak_ec_rate())
    print("Energy charge rate off peak: ", SimpleCost.get_off_peak_ec_rate())
    print("Demand charge rate on peak: ", SimpleCost.get_on_peak_dc_rate())
    print("Demand charge rate off peak: ", SimpleCost.get_off_peak_dc_rate())








