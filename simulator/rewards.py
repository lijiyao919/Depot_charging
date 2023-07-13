from abc import ABC, abstractmethod
from simulator.time import Timer
from simulator.ev import EV
import numpy as np

class Reward(ABC):
    @abstractmethod
    def feedback(self, ev):
        raise NotImplementedError("Virtual method not implemented.")

class SimpleReward(Reward):
    def feedback(self, ev, success_trip=False):
        r = -(ev.ec+ev.dc)
        if success_trip:
            r += 0
        elif Timer.is_trip_started():
            r -= 1000
        else:
            pass
        return r

#For test
if __name__=='__main__':
    reward = SimpleReward()
    ev = EV()
    Timer._time_step = 0
    ev.add_soc(60)
    print("EV's soc: ", ev.soc)
    print(f"reward feedback at time {Timer.get_time_step()}: ",  reward.feedback(ev))
    print()

    Timer._time_step = 360
    ev.add_soc(5)
    print("EV's soc: ", ev.soc)
    print(f"reward feedback at time {Timer.get_time_step()}: ",  reward.feedback(ev))
    print()

    Timer._time_step = 385
    ev.add_soc(600)
    print("EV's soc: ", ev.soc)
    print(f"reward feedback at time {Timer.get_time_step()}: ", reward.feedback(ev))
    print()

    Timer._time_step = 390
    ev.add_soc(0)
    print(f"reward feedback at time {Timer.get_time_step()}: ", reward.feedback(ev, True))
    ev.consume_soc_for_one_trip()
    print("EV's soc: ", ev.soc)