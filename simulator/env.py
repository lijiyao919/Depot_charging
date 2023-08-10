from simulator.time import Timer
from simulator.ev import EV
from simulator.rewards import SimpleReward
from collections import namedtuple

class Env:

    State = namedtuple('State', ["Time", "soc", "max_soc", "soc_for_one_trip"])
    Record = namedtuple('Record', ['time', 'soc', 'act'])

    def __init__(self):
        self._ev = EV()
        self._reward_model = SimpleReward()
        self._info = {}
        self._total_reward = 0
        self._num_success_trips = 0

    def reset(self):
        Timer.reset()
        self._ev.reset()
        self._total_reward = 0
        self._num_success_trips = 0
        self._reward_model.reset()
        return self._state(), self._info

    def step(self, act):
        #record before act
        rec = {}
        rec['time'] = Timer.get_time_step()
        rec['soc'] = self._ev.soc

        #run with act
        if Timer.is_trip_started() and self._ev.is_soc_sufficient_for_one_trip():
            self._ev.add_soc(0)
            rec['act'] = 0
            reward = self._reward_model.feedback(self._ev, True)
            self._num_success_trips += 1
            self._ev.consume_soc_for_one_trip()
            Timer.set_time_step(Timer.get_time_step() + Timer.get_operation_duration())
        else:
            self._ev.add_soc(act)
            rec['act'] = act
            reward = self._reward_model.feedback(self._ev)
            Timer.tick_time_step()

        self._total_reward += reward
        self._info['rec'] = Env.Record(**rec)
        if Timer.is_end_time():
            done = True
        else:
            done = False

        return self._state(), reward, done, self._info

    def show_performace_metrics(self):
        print(f"the energy cost: ${self._ev.total_ec}")
        print(f"the demand cost: ${self._ev.total_dc()}")
        print(f"total reward: {self._total_reward}")
        print(f"success trips: {self._num_success_trips}")

    def _state(self):
        return Env.State(Timer.get_time_step(), self._ev.soc, self._ev.max_soc, self._ev.soc_for_one_trip)

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
