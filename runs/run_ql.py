from algorithms.ql import QL_Agent
from algorithms.agent import Generic_Agent
from simulator.env import Env

TOTAL_EPISODE = 70000

def run_ql():
    env = Env()
    agent = QL_Agent()
    ep = 0
    exp = {}

    while ep < TOTAL_EPISODE:
        state, _ = env.reset()
        done = False
        while not done:
            act = agent.select_act(state, ep)
            next_state, reward, done, _ = env.step(act)
            exp["state"] = state
            exp["next_state"] = next_state
            exp["reward"] = reward
            exp["act"] = act
            agent.learn(exp)
            state = next_state
        print("The episode: ", ep)
        env.show_performace_metrics()
        print("\n")
        ep += 1
    return agent

if __name__=='__main__':
    ag = run_ql()
    Generic_Agent.plot_strategy(qlearning=ag)
    Generic_Agent.plot_soc(qlearning=ag)

