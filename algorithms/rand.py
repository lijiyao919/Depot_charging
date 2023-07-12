from algorithms.agent import Generic_Agent
from simulator.time import Timer
import random

class Rand_Agent(Generic_Agent):
    def select_act(self, state, ep):
        if state["soc"] - state["max_soc"] >= 0:
            act = 0
        else:
            act = random.choice(self.acts)
        self.soc_tracker.append((Timer.get_time_step(), state["soc"]))
        self.act_tracker.append((Timer.get_time_step(), act))
        return act