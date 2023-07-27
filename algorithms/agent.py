from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from simulator.time import Timer
import torch

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('The device is: ', device)

class Generic_Agent(ABC):
    def __init__(self):
        self.acts = [0, 50, 100, 150, 200, 250, 300, 350]
        self.act_tracker = []
        self.soc_tracker = []

    @abstractmethod
    def select_act(self, state, ep):
        raise NotImplementedError("select_act must be implemented in subclasses")

    @staticmethod
    def plot_strategy(**kwargs):
        for sol_name, sol_obj in kwargs.items():
            time_steps, acts = zip(*sol_obj.act_tracker)
            plt.plot(time_steps, acts, label=sol_name)
        xticks = range(Timer.get_start_time(), Timer.get_end_time()+2, 60)
        xticks_label = range(Timer.get_start_time()//60, Timer.get_end_time()//60+2)
        plt.xticks(xticks, xticks_label)
        plt.yticks(sol_obj.acts, sol_obj.acts)
        plt.xlabel("Time")
        plt.ylabel("Act (Kw)")
        plt.legend()
        plt.show()

    @staticmethod
    def plot_soc(**kwargs):
        for soc_name, soc_obj in kwargs.items():
            time_steps, socs = zip(*soc_obj.soc_tracker)
            plt.plot(time_steps, socs, label=soc_name)
        xticks = range(Timer.get_start_time(), Timer.get_end_time() + 2, 60)
        xticks_label = range(Timer.get_start_time() // 60, Timer.get_end_time() // 60 + 2)
        plt.xticks(xticks, xticks_label)
        plt.xlabel("Time")
        plt.ylabel("SoC (kWh)")
        plt.legend()
        plt.show()