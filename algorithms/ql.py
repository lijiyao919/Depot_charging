from collections import defaultdict
import numpy as np
import random
import math

acts = [0, 2, 4, 6]

ALPHA = 0.1
GAMMA = 0.99

EPS_START = 1
EPS_END = 0.001
EPS_DECAY = 4000

class QL_Agent:
    def __init__(self):
        self.Q = defaultdict(lambda : np.zeros(len(acts)))

    def select_act(self, state, ep):
        s = QL_Agent._state_transform(state)
        eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(-1. * ep / EPS_DECAY)
        if random.random() > eps_threshold:
            act_idx = np.argmax(self.Q[s])
            act = acts[act_idx]
            if act != 0:
                print(self.Q[s])
        else:
            #print("I play randomly", eps_threshold)
            act = random.choice(acts)
        return act,eps_threshold

    def learn(self, exp):
        s = QL_Agent._state_transform(exp["state"])
        next_s = QL_Agent._state_transform(exp["next_state"])
        r = exp["reward"]
        a_idx = acts.index(exp["act"])
        #print(r, s, next_s, a_idx, np.max(self.Q[next_s]), self.Q[s][a_idx])
        self.Q[s][a_idx] = self.Q[s][a_idx] + ALPHA * (r + GAMMA * np.max(self.Q[next_s]) - self.Q[s][a_idx])

    @staticmethod
    def _state_transform(state):
        return (state["Time"], round(state["max_soc"]-state["soc"], 2))