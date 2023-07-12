import configparser
from simulator.time import Timer
from simulator.cost import SimpleCost
import os

class EV:
    _config = configparser.ConfigParser()
    _config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    _config.read(_config_file)

    def __init__(self):
        self._max_soc = float(EV._config.get('EV', 'max_soc'))
        self._initial_soc = float(EV._config.get('EV', 'initial_soc'))
        self._soc_for_one_trip = float(EV._config.get('EV', 'soc_for_one_trip'))

        self._soc = self._initial_soc
        self._total_ec = 0
        self._total_dc = 0
        self._ec = 0
        self._dc = 0

    def reset(self):
        #self._soc = self._initial_soc
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

    @property
    def soc_for_one_trip(self):
        return self._soc_for_one_trip

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

    def is_soc_sufficient_for_one_trip(self):
        return self._soc >= self._soc_for_one_trip

    def consume_soc_for_one_trip(self):
        self._soc -= self._soc_for_one_trip
        assert self._soc >= 0

#For test
if __name__=='__main__':
    ev = EV()
    print(f"Max soc: {ev.max_soc}kWh")
    print(f"Initial soc: {ev.soc}kWh")
    print(f"soc for one trip: {ev.soc_for_one_trip}kWh")
    print()

    print("####Add Soc in unpeak hours####")
    ev.add_soc(90)
    print(f"soc after adding 90kW for {Timer.get_simulated_interval()} minutes: {ev.soc}kWh")
    print(f"energy charge: ${ev.ec}")
    print(f"demand charge0: ${ev.dc}")
    print(f"Total energy charge: ${ev.total_ec}")
    print(f"Total demand charge: ${ev.total_dc}")
    print(f"is sufficient for one trip: {ev.is_soc_sufficient_for_one_trip()}")
    print()

    print("####Add Soc in peak hours####")
    Timer._time_step = 1000
    ev.add_soc(480)
    print(f"soc after adding 480kW for {Timer.get_simulated_interval()} minutes: {ev.soc}kWh")
    print("energy charge:", ev.ec)
    print("demand charge0:", ev.dc)
    print("Total energy charge:", ev.total_ec)
    print("Total demand charge:", ev.total_dc)
    print(f"is sufficient for one trip: {ev.is_soc_sufficient_for_one_trip()}")
    ev.consume_soc_for_one_trip()
    print(f"The left soc is: ", ev.soc)
    print(f"is sufficient for one trip: {ev.is_soc_sufficient_for_one_trip()}")
    print()

    print("####Reset####")
    ev.reset()
    print(f"soc now after reset: ${ev.soc}")
    print(f"energy charge: ${ev.ec}")
    print(f"demand charge: ${ev.dc}")
    print(f"Total energy charge: ${ev.total_ec}")
    print(f"Total demand charge: ${ev.total_dc}")