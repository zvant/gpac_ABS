#!python3

import os
from model import torch, np, DQN

weights_filename = 'rl_weights.txt'
transitions_filename = 'rl_transitions.txt'
train_log_filename = 'rl_dqn.log'
command = 'bin\\x64\\release\\mp4client.exe -run-for 40 -exit -c GPAC.cfg -logs all@error:dash@debug -log-file dash.log "http://172.17.217.51/dash/dash.mpd"'

def train():
    model = DQN()

    for episode in range(0, 16):
        with open(transitions_filename, 'w') as fp:
            pass
        model.dump_weights(weights_filename)
        with open(weights_filename, 'a') as fp:
            fp.write('%f\n' % (0.85 ** episode))
        os.system(command)

        t, Xt, Rt, Xt1 = [], [], [], []
        with open(transitions_filename, 'r') as fp:
            lines = list(map(lambda l: l.strip(), fp.readlines()))
            assert (len(lines) % 4) == 0, 'corrupted transitions file: %s' % transitions_filename
            for idx in range(0, len(lines) // 4):
                t.append(int(lines[idx * 4].split(' ')[1]))
                Xt.append(list(map(float, lines[idx * 4 + 1].split(' '))))
                Rt.append(float(lines[idx * 4 + 2]))
                Xt1.append(list(map(float, lines[idx * 4 + 3].split(' '))))

        t, Xt, Rt, Xt1 = map(lambda l: np.array(l), [t, Xt, Rt, Xt1])
        loss = model.train_Xy(Xt, Rt, Xt1)

        with open(train_log_filename, 'a') as fp:
            fp.write('%d,%d,%f\n' % (episode, t.shape[0], loss))

if __name__ == '__main__':
    train()
