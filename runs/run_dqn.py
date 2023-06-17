from algorithms.dqn import DQN_Agent
from algorithms.agent import Generic_Agent
from simulator.env import Env

TOTAL_EPISODE = 30000

def run_dqn():
    env = Env()
    agent = DQN_Agent(30, 72, 128, 4, 0.001)
    ep = 0

    while ep < TOTAL_EPISODE:
        state, _ = env.reset()
        done = False
        while not done:
            act = agent.select_act(state, ep)
            next_state, reward, done, _ = env.step(act)
            agent.store_exp(state, act, reward, next_state)
            loss = agent.update(ep, done)
            state = next_state
        print("The episode: ", ep)
        env.show_performace_metrics()
        if done:
            print("the loss: ", loss.item())
        print("\n")
        ep += 1
    return agent

if __name__=='__main__':
    ag = run_dqn()
    #Generic_Agent.plot_strategy(dqn=ag)

