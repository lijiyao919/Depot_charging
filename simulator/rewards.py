from abc import ABC, abstractmethod
from simulator.time import Timer
from simulator.ev import EV

class Reward(ABC):
    @abstractmethod
    def feedback(self, ev):
        raise NotImplementedError("Virtual method not implemented.")

class SimpleReward(Reward):
    def feedback(self, ev):
        r = -(ev.ec+ev.dc)
        if Timer.is_end_time():
            r -= 0.01*(ev.max_soc-ev.soc)**2
        return r

#For test
if __name__=='__main__':
    reward = SimpleReward()
    ev = EV()
    ev.add_soc(600)
    print(reward.feedback(ev))

    Timer._time_step = 1000
    ev.add_soc(600)
    print(reward.feedback(ev))

    ev.reset()
    Timer._time_step = 1440
    ev.add_soc(60)
    print(reward.feedback(ev))