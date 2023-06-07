from simulator.env import Env
from algorithms.optim import Optim_Agent
def run_optim():
    env = Env()
    state, _ = env.reset()
    agent = Optim_Agent()
    while True:
        act = agent.select_act(state, None)
        next_state, reward, terminate, _ = env.step(act)
        state = next_state
        if terminate:
            break
    env.show_performace_metrics()

if __name__=='__main__':
    run_optim()