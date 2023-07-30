import configparser
from simulator.time import Timer
from simulator.cost import SimpleCost
from collections import deque
import os

kW_TRACK_UNIT = 3

class EV:
    _config = configparser.ConfigParser()
    _config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    _config.read(_config_file)

    def __init__(self):
        self._max_soc = float(EV._config.get('EV', 'max_soc'))
        self._initial_soc = float(EV._config.get('EV', 'initial_soc'))
        self._soc_for_one_trip = float(EV._config.get('EV', 'soc_for_one_trip'))
        self._track_kW = deque([], maxlen=kW_TRACK_UNIT)
        self._kW_max_on_peak = 0
        self._kW_max_off_peak = 0
        self._prev_peak = False

        self._soc = self._initial_soc
        self._total_ec = 0

    def reset(self):
        self._soc = self._initial_soc
        self._total_ec = 0
        self._kW_max_on_peak = 0
        self._kW_max_off_peak = 0
        self._prev_peak = False
        self._track_kW.clear()

    @property
    def max_soc(self):
        return self._max_soc

    @property
    def soc(self):
        return self._soc

    @property
    def total_ec(self):
        return self._total_ec

    @property
    def kW_max_on_peak(self):
        return self._kW_max_on_peak

    @property
    def kW_max_off_peak(self):
        return self._kW_max_off_peak

    def total_dc(self):
        return max(self._kW_max_on_peak * SimpleCost.get_on_peak_dc_rate(), self._kW_max_off_peak * SimpleCost.get_off_peak_dc_rate()) / kW_TRACK_UNIT

    @property
    def soc_for_one_trip(self):
        return self._soc_for_one_trip

    def add_soc(self, act):
        #start a trip
        if act is None:
            self._track_kW.clear()
            return

        #check if need to clear kW_track
        if (not self._prev_peak and Timer.is_peak_hours()) or (self._prev_peak and not Timer.is_peak_hours()):
            self._track_kW.clear()

        #add sOc
        soc_delta = act/Timer.get_units_in_one_hour()
        self._soc = self._soc+soc_delta if self._soc+soc_delta < self._max_soc else self._max_soc
        self._track_kW.append(act)

        #ec and dc
        if Timer.is_peak_hours():
            self._total_ec += SimpleCost.get_on_peak_ec_rate() * soc_delta
            self._kW_max_on_peak = max(self._kW_max_on_peak, sum(self._track_kW))
            self._prev_peak = True
        else:
            self._total_ec += SimpleCost.get_off_peak_ec_rate() * soc_delta
            self._kW_max_off_peak = max(self._kW_max_off_peak, sum(self._track_kW))
            self._prev_peak = False

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

    print("####Add None in SoC####")
    ev.add_soc(None)
    print(f"soc after adding None: {ev.soc}kWh")
    print(f"Total energy charge: ${ev.total_ec}")
    print(f"Total demand charge: ${ev.total_dc}")
    print()

    print("####Add Soc in off peak hours####")
    ev.add_soc(90)
    print(f"soc after adding 90kW for {Timer.get_simulated_interval()} minutes: {ev.soc}kWh")
    print(f"Total energy charge: ${ev.total_ec}")
    print(f"is sufficient for one trip: {ev.is_soc_sufficient_for_one_trip()}")
    print()

    print("####Add Soc in on peak hours####")
    Timer.set_time_step(1000)
    ev.add_soc(480)
    print(f"soc after adding 480kW for {Timer.get_simulated_interval()} minutes: {ev.soc}kWh")
    print("Total energy charge:", ev.total_ec)
    print(f"is sufficient for one trip: {ev.is_soc_sufficient_for_one_trip()}")
    ev.consume_soc_for_one_trip()
    print(f"The left soc is: ", ev.soc)
    print(f"is sufficient for one trip: {ev.is_soc_sufficient_for_one_trip()}")
    print()

    print("####Reset####")
    ev.reset()
    print(f"soc now after reset: ${ev.soc}")
    print(f"Total energy charge: ${ev.total_ec}")
    print(f"Total demand charge: ${ev.total_dc()}")
    print(f"max kW off peak: {ev.kW_max_off_peak}")
    print(f"max kW on peak: {ev.kW_max_on_peak}")
    print()

    print('#### Check DC off peak hours and off operation####')
    Timer.set_time_step(0)
    while Timer.get_time_step() <= 60:
        if Timer.get_time_step() == 30:
            ev.add_soc(40)
        else:
            ev.add_soc(10)
        Timer.tick_time_step()
    print(f"max kW off peak: {ev.kW_max_off_peak}")
    print(f"max kW on peak: {ev.kW_max_on_peak}")
    print(f"total dc: {ev.total_dc()}")
    print()

    print('#### Check DC off peak hours and on operation####')
    Timer.set_time_step(360)
    while Timer.get_time_step() < 480:
        if Timer.get_time_step() == 390:
            ev.add_soc(None)
            Timer.set_time_step(415)
        elif Timer.get_time_step() == 420:
            ev.add_soc(None)
            Timer.set_time_step(445)
        else:
            if Timer.get_time_step() == 380:
                ev.add_soc(50)
            elif Timer.get_time_step() == 385:
                ev.add_soc(100)
            elif Timer.get_time_step() == 415:
                ev.add_soc(200)
            else:
                ev.add_soc(10)
            Timer.tick_time_step()
    print(f"max kW off peak: {ev.kW_max_off_peak}")
    print(f"max kW on peak: {ev.kW_max_on_peak}")
    print(f"total dc: {ev.total_dc()}")
    print()

    print('#### Check DC on peak hours and off operation####')
    Timer.set_time_step(1140)
    while Timer.get_time_step() <= 1200:
        if Timer.get_time_step() == 1170:
            ev.add_soc(40)
        else:
            ev.add_soc(10)
        Timer.tick_time_step()
    print(f"max kW off peak: {ev.kW_max_off_peak}")
    print(f"max kW on peak: {ev.kW_max_on_peak}")
    print(f"total dc: {ev.total_dc()}")
    print()

    print('#### Check DC on peak hours and on operation####')
    Timer.set_time_step(780)
    while Timer.get_time_step() < 900:
        if Timer.get_time_step() == 810:
            ev.add_soc(None)
            Timer.set_time_step(835)
        elif Timer.get_time_step() == 840:
            ev.add_soc(None)
            Timer.set_time_step(865)
        else:
            if Timer.get_time_step() == 800:
                ev.add_soc(50)
            elif Timer.get_time_step() == 805:
                ev.add_soc(100)
            elif Timer.get_time_step() == 835:
                ev.add_soc(200)
            else:
                ev.add_soc(10)
            Timer.tick_time_step()
    print(f"max kW off peak: {ev.kW_max_off_peak}")
    print(f"max kW on peak: {ev.kW_max_on_peak}")
    print(f"total dc: {ev.total_dc()}")
    print()

    print('#### Check DC: transit from off peak hours to on peak hour (on operation)####')
    ev.reset()
    Timer.set_time_step(770)
    while Timer.get_time_step() < 810:
        if Timer.get_time_step() == 780:
            ev.add_soc(None)
            Timer.set_time_step(800)
        else:
            if Timer.get_time_step() == 775:
                ev.add_soc(200)
            else:
                ev.add_soc(10)
            Timer.tick_time_step()
    print(f"max kW off peak: {ev.kW_max_off_peak}")
    print(f"max kW on peak: {ev.kW_max_on_peak}")
    print(f"total dc: {ev.total_dc()}")
    print()

    print('#### Check DC: transit from on peak hours to off peak hour (off operation)####')
    ev.reset()
    Timer.set_time_step(1250)
    while Timer.get_time_step() < 1290:
        if Timer.get_time_step() == 1255:
            ev.add_soc(200)
        else:
            ev.add_soc(10)
        Timer.tick_time_step()
    print(f"max kW off peak: {ev.kW_max_off_peak}")
    print(f"max kW on peak: {ev.kW_max_on_peak}")
    print(f"total dc: {ev.total_dc()}")
    print()