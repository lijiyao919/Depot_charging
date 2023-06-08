from collections import defaultdict
import numpy as np
import random
import math
from algorithms.agent import Generic_Agent

ALPHA = 0.1
GAMMA = 0.99

EPS_START = 1
EPS_END = 0
EPS_DECAY = 4000

class QL_Agent(Generic_Agent):
    def __init__(self):
        super().__init__()
        self.Q = defaultdict(lambda : np.zeros(len(self.acts)))

    def select_act(self, state, ep):
        s = QL_Agent._state_transform(state)
        eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(-1. * ep / EPS_DECAY)
        if random.random() > eps_threshold:
            act_idx = np.argmax(self.Q[s])
            act = self.acts[act_idx]
        else:
            act = random.choice(self.acts)
        if ep == 29999:
            self.act_tracker.append(act)
        return act

    def learn(self, exp):
        s = QL_Agent._state_transform(exp["state"])
        next_s = QL_Agent._state_transform(exp["next_state"])
        r = exp["reward"]
        a_idx = self.acts.index(exp["act"])
        #print(r, s, next_s, a_idx, np.max(self.Q[next_s]), self.Q[s][a_idx])
        self.Q[s][a_idx] = self.Q[s][a_idx] + ALPHA * (r + GAMMA * np.max(self.Q[next_s]) - self.Q[s][a_idx])

    @staticmethod
    def _state_transform(state):
        return (state["Time"], round(state["max_soc"]-state["soc"], 1))