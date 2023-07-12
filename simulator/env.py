from simulator.time import Timer
from simulator.ev import EV
from simulator.rewards import SimpleReward

class Env:
    def __init__(self):
        self._ev = EV()
        self._reward_model = SimpleReward()
        self._info = {}

    def reset(self):
        Timer.reset()
        self._ev.reset()
        return self._state(), self._info

    def step(self, act):
        if Timer.is_trip_started() and self._ev.is_soc_sufficient_for_one_trip():
            self._ev.consume_soc_for_one_trip()
            reward = self._reward_model.feedback(self._ev)
            Timer.set_time_step(Timer.get_time_step() + Timer.get_operation_duration())
        else:
            self._ev.add_soc(act)
            reward = self._reward_model.feedback(self._ev)
            Timer.tick_time_step()

        if Timer.is_end_time():
            done = True
        else:
            done = False

        return self._state(), reward, done, self._info

    def show_performace_metrics(self):
        print("the cost (ec+dc): ", self._ev.total_ec+self._ev.total_dc)
        print("the SoC (kWh): ", self._ev.soc)

    def _state(self):
        return {"Time": Timer.get_time_step(), "soc":self._ev.soc, "max_soc":self._ev.max_soc}

#For test
if __name__=='__main__':
    env = Env()
    print("reset the env: ", env.reset())
    print(f"step the env at {Timer.get_time_step()}: ", env.step(600))
    Timer.set_time_step(360)
    print(f"step the env at {Timer.get_time_step()}: ", env.step(600))
    print(f"step the env at {Timer.get_time_step()}: ", env.step(90))
    print(f"step the env at {Timer.get_time_step()}: ", env.step(90))
    Timer.set_time_step(1435)
    print(f"step the env at {Timer.get_time_step()}: ", env.step(90))
