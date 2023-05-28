from simulator.time import Timer
from simulator.ev import EV
from simulator.rewards import SimpleReward

class Env:
    def __init__(self):
        self._ev = EV()
        self._reward_model = SimpleReward()

    def reset(self):
        Timer.reset()
        #self._ev.reset()
        return self._state()

    def step(self, act):
        self._ev.add_soc(act)
        reward = self._reward_model.feedback(self._ev)
        terminated = Timer.is_end_time()
        Timer.tick_time_step()
        return self._state(), reward, terminated

    def _state(self):
        return {"Time": Timer.get_time_step(), "soc":self._ev.soc}

#For test
if __name__=='__main__':
    env = Env()
    print(env.reset())
    print(env.step(600))
