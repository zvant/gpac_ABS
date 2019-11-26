#!python3

import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.optim as optim

import numpy as np
from sklearn.utils import shuffle

class DQN(nn.Module):
    def __init__(self):
        super(DQN, self).__init__()
        if torch.cuda.is_available():
            self.float = torch.cuda.DoubleTensor
            self.long = torch.cuda.LongTensor
        else:
            self.float = torch.DoubleTensor
            self.long = torch.LongTensor

        self.input_dim = 5 * 3
        self.hidden_dim = 32
        self.output_dim = 4
        self.fc1 = nn.Linear(self.input_dim, self.hidden_dim)
        self.fc2 = nn.Linear(self.hidden_dim, self.hidden_dim)
        self.fc3 = nn.Linear(self.hidden_dim, self.output_dim)
        self.a1 = nn.ReLU()
        self.a2 = nn.ReLU()
        self.activate_desc = 'r'
        # self.a1 = nn.Sigmoid()
        # self.a2 = nn.Sigmoid()
        # self.activate_desc = 's'

        self.loss_fn = nn.MSELoss()
        self.init_weights()
        self.lr = 0.5e-3
        self.optimizer = optim.Adam(self.parameters(), lr=self.lr)
        self.gamma = 0.85
        self.type(self.float)

    def init_weights(self):
        self.apply(lambda m: m.reset_parameters() if hasattr(m, 'reset_parameters') else None)
        self.apply(lambda m: nn.init.xavier_uniform_(m.weight.data) if isinstance(m, nn.Linear) else None)

    def forward(self, X):
        X = self.fc1(X)
        X = self.a1(X)
        X = self.fc2(X)
        X = self.a2(X)
        return self.fc3(X)

    def train_Xy(self, Xt, At, Rt, Xt1, batchsize=None):
        N = Xt.shape[0]
        if batchsize is None:
            batchsize = N
        Xt, At, Rt, Xt1 = shuffle(Xt, At, Rt, Xt1)
        Xt, Rt, Xt1 = map(lambda arr: torch.from_numpy(arr).type(self.float), [Xt, Rt, Xt1])
        At = torch.from_numpy(At).type(self.long)

        avg_loss = []

        for idx in range(0, N // batchsize):
            a = At[idx * batchsize : (idx + 1) * batchsize]
            y = self(Xt[idx * batchsize : (idx + 1) * batchsize])
            r = Rt[idx * batchsize : (idx + 1) * batchsize]
            for iy in range(0, batchsize):
                y[iy][0] = y[iy][a[iy]]
            y = y[:, 0]

            xp = Xt1[idx * batchsize : (idx + 1) * batchsize]
            yp = self(xp)
            yp, _ = yp.max(dim=1)
            yp = yp.view(batchsize,)

            L = self.loss_fn(r + self.gamma * yp, y)
            self.optimizer.zero_grad()
            L.backward()
            self.optimizer.step()
            avg_loss.append(float(L.detach().cpu().numpy()) / batchsize)

        return np.array(avg_loss).mean()

    def dump_weights(self, filename):
        with open(filename, 'w') as fp:
            fp.write('%d %d %d %d\n' % (self.input_dim, self.hidden_dim, self.hidden_dim, self.output_dim))
            for l in self.fc1.weight.data.cpu().numpy():
                fp.write('%s\n' % ' '.join(map(str, l.tolist())))
            for x in self.fc1.bias.data.cpu().numpy():
                fp.write('%s\n' % x)
            for l in self.fc2.weight.data.cpu().numpy():
                fp.write('%s\n' % ' '.join(map(str, l.tolist())))
            for x in self.fc2.bias.data.cpu().numpy():
                fp.write('%s\n' % x)
            for l in self.fc3.weight.data.cpu().numpy():
                fp.write('%s\n' % ' '.join(map(str, l.tolist())))
            for x in self.fc3.bias.data.cpu().numpy():
                fp.write('%s\n' % x)
