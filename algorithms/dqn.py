from algorithms.models.mlp import MLP
from algorithms.agent import Generic_Agent
from algorithms.agent import device
from collections import namedtuple
from collections import deque
import torch.nn as nn
import numpy as np
import random
import math
import torch

EPS_START = 1
EPS_END = 0
EPS_DECAY = 4000

Transition = namedtuple('Transition', ('state', 'act_idx', 'reward', 'next_state')) #Transition is a class, not object

class ReplayBuffer(object):
    def __init__(self, capacity):
        self.buffer = deque([], maxlen=capacity)

    def push(self, *args):
        self.buffer.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        return len(self.buffer)

class DQN_Agent(Generic_Agent):
    def __init__(self, embed_dims, time_dims, hidden_dims, n_actions, eta, buffer_size=10000, batch_size=32, target_update_feq=500):
        super(DQN_Agent, self).__init__()
        self.replay_buffer = ReplayBuffer(buffer_size)
        self.gamma = 0.99
        self.batch_size = batch_size
        self.target_update = target_update_feq

        self.policy_net = MLP(embed_dims, time_dims, hidden_dims, n_actions, eta).to(device)
        self.target_net = MLP(embed_dims, time_dims, hidden_dims, n_actions, eta).to(device)

        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

    def store_exp(self, state, act, reward, next_state):
        state = self._state_transform(state)
        next_state = self._state_transform(next_state)
        act_idx = self.acts.index(act)
        self.replay_buffer.push(state, [act_idx], [reward], next_state)

    def select_act(self, state, ep):
        state = self._state_transform(state)
        eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(-1. * ep / EPS_DECAY)
        if random.random() > eps_threshold:
            act_score = self.policy_net(state)
            act_idx = act_score.max(dim=1)[1]
            act = self.acts[act_idx]
        else:
            act = random.choice(self.acts)
        if ep == 29999:
            self.act_tracker.append(act)
        return act

    def update(self, ep, done):
        if len(self.replay_buffer) < self.batch_size:
            return

        samples = self.replay_buffer.sample(self.batch_size)
        #print(samples)

        batch = Transition(*zip(*samples))
        state_batch = np.concatenate(batch.state,axis=0)
        next_state_batch = np.concatenate(batch.next_state, axis=0)
        act_idx_batch = np.concatenate(batch.act_idx).reshape(self.batch_size, 1)
        reward_batch = np.concatenate(batch.reward).reshape(self.batch_size, 1)
        #print(act_idx_batch)
        #print(reward_batch)

        st_act_values = self.policy_net(state_batch).gather(dim=1, index=torch.tensor(act_idx_batch, dtype=torch.int64).to(device))
        next_st_act_values = self.target_net(next_state_batch).max(1)[0].detach().reshape(self.batch_size, 1)
        if done:
            target_st_act_values = torch.tensor(reward_batch).to(device)
        else:
            target_st_act_values = torch.tensor(reward_batch).to(device) + self.gamma * next_st_act_values


        # compute huber loss and optimize
        criterion = nn.SmoothL1Loss()
        loss = criterion(st_act_values, target_st_act_values)
        self.policy_net.optimizer.zero_grad()
        loss.backward()
        for param in self.policy_net.parameters():
            param.grad.data.clamp_(-1, 1)
        self.policy_net.optimizer.step()

        if ep % self.target_update == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())

        return loss

    @staticmethod
    def _state_transform(state):
        return [(state["Time"], state["soc"]/state["max_soc"])]

ag = DQN_Agent(30, 72, 128, 4, 0.001)
#ag.select_act({"Time": 1440, "soc":5, "max_soc":24}, 0)
ag.store_exp({"Time": 720, "soc":5, "max_soc":24}, 0, 0, {"Time": 730, "soc":5.1, "max_soc":24})
ag.store_exp({"Time": 730, "soc":5.1, "max_soc":24}, 2, -0.3, {"Time": 740, "soc":6, "max_soc":24})
#ag.update(0)