from abc import ABC, abstractmethod
from simulator.time import Timer
from simulator.ev import EV
from simulator.cost import SimpleCost

class Reward(ABC):
    @abstractmethod
    def feedback(self, ev):
        raise NotImplementedError("Virtual method not implemented.")

class SimpleReward(Reward):
    def __init__(self):
        self._soc_delta_max_on_peak = 0
        self._soc_delta_max_off_peak = 0

    def feedback(self, ev, success_trip=False):
        r = 0
        if success_trip:
            r += 0
        else:
            if Timer.is_trip_started():
                r -= 1000
            if Timer.is_peak_hours():
                r -= ev.soc_delta * SimpleCost.get_on_peak_ec_rate() + max(0, ev.soc_delta-self._soc_delta_max_on_peak) * SimpleCost.get_on_peak_dc_rate()
                if ev.soc_delta > self._soc_delta_max_on_peak:
                    self._soc_delta_max_on_peak = ev.soc_delta
            else:
                r -= ev.soc_delta * SimpleCost.get_off_peak_ec_rate()+ max(0, ev.soc_delta-self._soc_delta_max_off_peak) * SimpleCost.get_off_peak_dc_rate()
                if ev.soc_delta > self._soc_delta_max_off_peak:
                    self._soc_delta_max_off_peak = ev.soc_delta
        return r

#For test
if __name__=='__main__':
    reward = SimpleReward()
    ev = EV()

    print("#### off peak hour, off operation 1####")
    Timer._time_step = 0
    ev.add_soc(60)
    print("EV's soc: ", ev.soc)
    print(f"reward feedback at time {Timer.get_time_step()}: ",  reward.feedback(ev))
    print()

    print("#### off peak hour, off operation 2####")
    Timer._time_step = 5
    ev.add_soc(70)
    print("EV's soc: ", ev.soc)
    print(f"reward feedback at time {Timer.get_time_step()}: ", reward.feedback(ev))
    print()

    print("#### off peak hour, on operation,  success trip####")
    Timer._time_step = 360
    ev.add_soc(None)
    print("EV's soc: ", ev.soc)
    print(f"reward feedback at time {Timer.get_time_step()}: ",  reward.feedback(ev, True))
    print()

    print("#### off peak hour, on operation,  rest####")
    Timer._time_step = 385
    ev.add_soc(80)
    print("EV's soc: ", ev.soc)
    print(f"reward feedback at time {Timer.get_time_step()}: ", reward.feedback(ev))
    print()

    print("#### off peak hour, on operation,  fail trip####")
    Timer._time_step = 390
    ev.add_soc(60)
    print("EV's soc: ", ev.soc)
    print(f"reward feedback at time {Timer.get_time_step()}: ", reward.feedback(ev))
    print()

    print("#### on peak hour, on operation, success trip####")
    Timer._time_step = 780
    ev.add_soc(None)
    print("EV's soc: ", ev.soc)
    print(f"reward feedback at time {Timer.get_time_step()}: ", reward.feedback(ev, True))
    print()

    print("#### on peak hour, on operation, rest####")
    Timer._time_step = 805
    ev.add_soc(60)
    print("EV's soc: ", ev.soc)
    print(f"reward feedback at time {Timer.get_time_step()}: ", reward.feedback(ev))
    print()

    print("#### on peak hour, on operation, fail trip 1####")
    Timer._time_step = 810
    ev.add_soc(48)
    print("EV's soc: ", ev.soc)
    print(f"reward feedback at time {Timer.get_time_step()}: ", reward.feedback(ev))
    print()

    print("#### on peak hour, on operation, fail trip 2####")
    Timer._time_step = 815
    ev.add_soc(72)
    print("EV's soc: ", ev.soc)
    print(f"reward feedback at time {Timer.get_time_step()}: ", reward.feedback(ev))
    print()

