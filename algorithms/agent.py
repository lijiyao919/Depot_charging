from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from simulator.time import Timer
import numpy as np

class Generic_Agent(ABC):
    def __init__(self):
        self.act_tracker = []

    @abstractmethod
    def select_act(self, state, ep):
        raise NotImplementedError("select_act must be implemented in subclasses")

    @staticmethod
    def plot_strategy(**kwargs):
        time_step = range(Timer.get_start_time(), Timer.get_end_time()+1, Timer.get_simulated_interval())
        for sol_name, sol_obj in kwargs.items():
            plt.plot(time_step, sol_obj.act_tracker, label=sol_name)
        xticks = range(Timer.get_start_time(), Timer.get_end_time()+1, 60)
        xticks_label = range(Timer.get_start_time()//60, Timer.get_end_time()//60+1)
        plt.xticks(xticks, xticks_label)
        plt.xlabel("Time")
        plt.ylabel("Act (Kw)")
        plt.legend()
        plt.show()