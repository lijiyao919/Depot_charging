from abc import ABC, abstractmethod
from simulator.time import Timer
from simulator.ev import EV
import numpy as np

class Reward(ABC):
    @abstractmethod
    def feedback(self, ev):
        raise NotImplementedError("Virtual method not implemented.")

class SimpleReward(Reward):
    def feedback(self, ev):
        if Timer.is_trip_started():
            if ev.is_soc_sufficient_for_one_trip():
                return 0
            else:
                return -1000
        else:
            return -(ev.ec+ev.dc)

#For test
if __name__=='__main__':
    reward = SimpleReward()
    ev = EV()
    ev.add_soc(600)
    print("EV's soc: ", ev.soc)
    print(f"reward feedback at time {Timer.get_time_step()}: ",  reward.feedback(ev))
    print()

    Timer._time_step = 360
    print("EV's soc: ", ev.soc)
    print(f"reward feedback at time {Timer.get_time_step()}: ",  reward.feedback(ev))
    print()

    Timer._time_step = 385
    ev.add_soc(600)
    print("EV's soc: ", ev.soc)
    print(f"reward feedback at time {Timer.get_time_step()}: ", reward.feedback(ev))
    print()

    Timer._time_step = 390
    ev.consume_soc_for_one_trip()
    ev.consume_soc_for_one_trip()
    print("EV's soc: ", ev.soc)
    print(f"reward feedback at time {Timer.get_time_step()}: ", reward.feedback(ev))