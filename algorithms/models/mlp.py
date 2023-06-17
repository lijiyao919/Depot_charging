import torch
import torch.nn as nn
import torch.optim as optim
from simulator.time import Timer
from algorithms.agent import device

class MLP(nn.Module):
    def __init__(self, embed_dims, time_dims, hidden_dims, n_actions, eta):
        super(MLP, self).__init__()
        self.embed = nn.Linear(1, embed_dims)
        self.hidden = nn.Linear(time_dims+embed_dims+1, hidden_dims)
        self.out = nn.Linear(hidden_dims, n_actions)
        self.non_linearity = nn.Sigmoid()

        self.optimizer = optim.RMSprop(self.parameters(), lr=eta)    #0.0001
        self.optimizer.zero_grad()

    def forward(self, state):
        time = []
        vol = []

        #extract from state
        for t, v in state:
            time.append(int(t))
            vol.append(v)

        #one-hot endcoding for time
        t_vec_len = (Timer.get_end_time() - Timer.get_start_time()) // Timer.get_simulated_interval()
        t_vec = torch.zeros(len(time), t_vec_len+1).to(device)
        for i, t in enumerate(time):
            t_vec[i][(t-Timer.get_start_time())//Timer.get_simulated_interval()] = 1
        #print("t vector: ", t_vec)

        #embed battery volumne
        v_vec = torch.zeros(len(vol), 1).to(device)
        for i, v in enumerate(vol):
            v_vec[i][0] = v
        #print("v_vec: ", v_vec)
        v_embed = self.embed(v_vec)
        #print("v_embed: ", v_embed)

        #concat t_vec and v_vec
        input_v = torch.cat((t_vec, v_embed), dim=1).to(device)
        #print("input vector: ", input_v)

        #feed forward
        x = self.hidden(input_v)
        x = self.non_linearity(x)
        action_scores = self.out(x)
        return action_scores

#For Test
if __name__=='__main__':
    mlp = MLP(30, 72, 128, 4, 0.001).to(device)
    print(mlp([(1440, 0.8), (720, 0.5), (800, 0.68)]))
