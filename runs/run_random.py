from simulator.env import Env
import random

actions = [0, 2, 4, 6]

def run_random():
    env = Env()
    state, _ = env.reset()
    while True:
        if state["max_soc"] - state["soc"] == 0:
            act = 0
        else:
            act = random.choice(actions)
        next_state, reward, terminate, _ = env.step(act)
        state = next_state
        if terminate:
            break
    env.show_performace_metrics()

if __name__=='__main__':
    run_random()
        