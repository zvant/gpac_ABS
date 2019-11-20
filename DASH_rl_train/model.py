#!python3

import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.optim as optim

import numpy as np

class DQN(nn.Module):
    def __init__(self):
        super(DQN, self).__init__()
        if torch.cuda.is_available():
            self.float = torch.cuda.FloatTensor
            self.long = torch.cuda.LongTensor
        else:
            self.float = torch.FloatTensor
            self.long = torch.LongTensor

        self.input_dim = 5 * 3 + 1
        self.hidden_dim = 32
        self.fc1 = nn.Linear(self.input_dim, self.hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(self.hidden_dim, 1)

        self.loss_fn = nn.MSELoss()
        self.init_weights()
        self.lr = 1.0e-3
        self.optimizer = optim.Adam(self.parameters(), lr=self.lr)
        self.type(self.float)

    def init_weights(self):
        self.apply(lambda m: m.reset_parameters() if hasattr(m, 'reset_parameters') else None)
        self.apply(lambda m: nn.init.xavier_uniform_(m.weight.data) if isinstance(m, nn.Linear) else None)

    def forward(self, X):
        X = self.fc1(X)
        X = self.relu(X)
        return self.fc2(X)

    def train_Xy(self, X, y, epochs):
        pass

    def dump_weights(self, filename):
        with open(filename, 'w') as fp:
            fp.write('%d %d\n' % (self.input_dim, self.hidden_dim))
            for l in self.fc1.weight.data.cpu().numpy():
                fp.write('%s\n' % ' '.join(map(str, l.tolist())))
            for x in self.fc1.bias.data.cpu().numpy():
                fp.write('%s\n' % x)
            fp.write('%d %d\n' % (self.hidden_dim, 1))
            fp.write('%s\n' % ' '.join(map(str, self.fc2.weight.data.cpu().numpy()[0].tolist())))
            fp.write('%s\n' % self.fc2.bias.data.cpu().numpy()[0])
