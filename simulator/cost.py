import configparser
from simulator.time import Timer


class SimpleCost:
    config = configparser.ConfigParser()
    config.read('config.ini')

    _on_peak_ec_rate = float(config.get('Cost', 'on_peak_ec_rate'))
    _off_peak_ec_rate = float(config.get('Cost', 'off_peak_ec_rate'))
    _on_peak_dc_rate = float(config.get('Cost', 'on_peak_dc_rate')) / Timer.get_per_time()
    _off_peak_dc_rate = float(config.get('Cost', 'off_peak_dc_rate')) / Timer.get_per_time()

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








