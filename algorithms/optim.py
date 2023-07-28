from simulator.time import Timer
from algorithms.agent import Generic_Agent

class Optim_Agent(Generic_Agent):
    def select_act(self, state, ep):
        if Timer.is_trip_started() and state.soc >= state.soc_for_one_trip:
            act = 0
        else:
            if 0<= Timer.get_time_step()<60:
                act = 350
            elif 360 <= Timer.get_time_step() < 720:
                act = 350
            elif 720 <= Timer.get_time_step() < 780:
                act = 120
            else:
                act = 0
        self.soc_tracker.append((Timer.get_time_step(), state.soc))
        self.act_tracker.append((Timer.get_time_step(), act))
        return act
