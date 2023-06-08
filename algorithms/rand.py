from algorithms.agent import Generic_Agent
import random

class Rand_Agent(Generic_Agent):
    def select_act(self, state, ep):
        if state["max_soc"] - state["soc"] == 0:
            act = 0
        else:
            act = random.choice(self.acts)
        self.act_tracker.append(act)
        return act