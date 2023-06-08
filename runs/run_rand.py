from simulator.env import Env
from algorithms.rand import Rand_Agent
from algorithms.agent import Generic_Agent
def run_rand():
    env = Env()
    agent = Rand_Agent()
    state, _ = env.reset()
    while True:
        act = agent.select_act(state, None)
        next_state, reward, terminate, _ = env.step(act)
        state = next_state
        if terminate:
            break
    env.show_performace_metrics()
    return agent

if __name__=='__main__':
    ag = run_rand()
    Generic_Agent.plot_strategy(rand=ag)
        