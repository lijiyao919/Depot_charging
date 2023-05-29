from simulator.env import Env
from simulator.time import Timer

def run_optim():
    env = Env()
    state, _ = env.reset()
    while True:
        if Timer.is_peak_hours() or state["max_soc"] - state["soc"] == 0:
           act = 0
        else:
            soc_delta = state["max_soc"] - state["soc"]
            if soc_delta >= 6 / Timer.get_per_time():
                act = 6
            elif soc_delta >= 4 / Timer.get_per_time():
                act = 4
            else:
                act = 2
        next_state, reward, terminate, _ = env.step(act)
        state = next_state
        if terminate:
            break
    env.show_performace_metrics()

if __name__=='__main__':
    run_optim()