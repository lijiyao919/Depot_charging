import configparser
from simulator.time import Timer
from simulator.cost import SimpleCost
import os
class EV:
    def __init__(self):
        _config = configparser.ConfigParser()
        _config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
        _config.read(_config_file)

        self._max_soc = float(_config.get('EV', 'max_soc'))
        self._initial_soc = float(_config.get('EV', 'initial_soc'))

        self._soc = self._initial_soc
        self._total_ec = 0
        self._total_dc = 0
        self._ec = 0
        self._dc = 0

    def reset(self):
        self._soc = self._initial_soc
        self._total_ec = 0
        self._total_dc = 0
        self._ec = 0
        self._dc = 0

    @property
    def max_soc(self):
        return self._max_soc

    @property
    def soc(self):
        return self._soc

    @property
    def ec(self):
        return self._ec

    @property
    def dc(self):
        return self._dc

    @property
    def total_ec(self):
        return self._total_ec

    @property
    def total_dc(self):
        return self._total_dc

    def add_soc(self, act):
        soc_delta = act/Timer.get_units_in_one_hour()
        self._soc = self._soc+soc_delta if self._soc+soc_delta < self._max_soc else self._max_soc

        if Timer.is_peak_hours():
            self._ec = SimpleCost.get_on_peak_ec_rate() * soc_delta
            self._dc = (SimpleCost.get_on_peak_dc_rate() * act) / Timer.get_units_in_one_hour()
        else:
            self._ec = SimpleCost.get_off_peak_ec_rate() * soc_delta
            self._dc = (SimpleCost.get_off_peak_dc_rate() * act) / Timer.get_units_in_one_hour()
        self._total_ec += self._ec
        self._total_dc += self._dc

#For test
if __name__=='__main__':
    ev = EV()
    print("Max soc: ", ev.max_soc)
    print("Initial soc now: ", ev.soc)
    ev.add_soc(6)
    print("soc now: ", ev.soc)
    print("energy charge:", ev.ec)
    print("demand charge0:", ev.dc)
    print("Total energy charge:", ev.total_ec)
    print("Total demand charge0:", ev.total_dc)

    Timer._time_step = 1000
    ev.add_soc(120)
    print("soc now: ", ev.soc)
    print("energy charge:", ev.ec)
    print("demand charge0:", ev.dc)
    print("Total energy charge:", ev.total_ec)
    print("Total demand charge:", ev.total_dc)

    ev.reset()
    print("soc now after reset: ", ev.soc)
    print("Total energy charge:", ev.total_ec)
    print("Total demand charge:", ev.total_dc)