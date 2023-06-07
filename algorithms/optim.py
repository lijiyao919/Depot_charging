from simulator.time import Timer
from algorithms.agent import Generic_Agent
class Optim_Agent(Generic_Agent):
    def select_act(self, state, ep):
        if Timer.is_peak_hours() or state["max_soc"] - state["soc"] == 0:
           act = 0
        else:
            soc_delta = state["max_soc"] - state["soc"]
            if soc_delta >= 6 / Timer.get_units_in_one_hour():
                act = 6
            elif soc_delta >= 4 / Timer.get_units_in_one_hour():
                act = 4
            else:
                act = 2
        self.act_tracker.append(act)
        return act

a = Optim_Agent()