from algorithms.ql import QL_Agent
from simulator.env import Env

TOTAL_EPISODE = 100000

def run_ql():
    env = Env()
    agent = QL_Agent()
    ep = 0
    exp = {}

    while ep < TOTAL_EPISODE:
        state, _ = env.reset()
        done = False
        while not done:
            act, eps_th = agent.select_act(state, ep)
            next_state, reward, done, _ = env.step(act)
            exp["state"] = state
            exp["next_state"] = next_state
            exp["reward"] = reward
            exp["act"] = act
            agent.learn(exp)
            state = next_state
        print("The episode: ", ep, eps_th)
        env.show_performace_metrics()
        print("\n")
        ep += 1

if __name__=='__main__':
    run_ql()

