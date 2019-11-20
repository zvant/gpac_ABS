#!python3

from model import torch, np, DQN

def train():
    model = DQN()
    model.dump_weights('rl_weights.txt')

if __name__ == '__main__':
    train()
