from simulator.env import Env
import random

actions = [0, 2, 4, 6]

def run_random():
    env = Env()
    state = env.reset()
    while True:
        act = random.choice(actions)
        next_state, reward, terminate = env.step(act)
        if terminate:
            break
    env.show_performace_metrics()

if __name__=='__main__':
    run_random()
        