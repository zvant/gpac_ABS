#!python3

import os
import shutil
from model import torch, np, DQN

weights_filename = 'rl_weights.txt'
transitions_filename = 'rl_transitions.txt'
train_log_filename = 'rl_dqn.log'
command = 'bin\\x64\\release\\mp4client.exe -run-for 60 -exit -c GPAC.cfg -logs all@error:dash@debug -log-file dash.log "http://172.17.217.51/dash/dash.mpd"'

def train():
    model = DQN()
    print('Verify')
    X_verify = np.array(range(0, 15), dtype=np.int)
    X_verify = (X_verify % 2) * 2 - 1.0
    X_verify = torch.from_numpy(X_verify).type(model.float)
    print(X_verify)
    print(model(X_verify))

    for episode in range(0, 5):
        model.dump_weights(weights_filename)
        with open(weights_filename, 'a') as fp:
            fp.write('%f %s\n' % (0.95 ** episode, model.activate_desc))
        if (episode % 5) == 0:
            shutil.copyfile(weights_filename, 'rl_dqn_model_ep_%d.txt' % episode)
        if (episode % 2) == 0:
            with open(transitions_filename, 'w') as fp:
                pass
        os.system(command)

        t, Xt, At, Rt, Xt1 = [], [], [], [], []
        with open(transitions_filename, 'r') as fp:
            lines = list(map(lambda l: l.strip(), fp.readlines()))
            if len(lines) < 12:
                print('Not enough data for training, skipped')
                continue
            assert (len(lines) % 4) == 0, 'corrupted transitions file: %s' % transitions_filename
            for idx in range(0, len(lines) // 4):
                t.append(int(lines[idx * 4].split(' ')[1]))
                Xt.append(list(map(float, lines[idx * 4 + 1].split(' '))))
                a, r = map(float, lines[idx * 4 + 2].split(' '))
                At.append(a)
                Rt.append(r)
                Xt1.append(list(map(float, lines[idx * 4 + 3].split(' '))))

        t, Xt, Rt, Xt1 = map(lambda l: np.array(l, dtype=np.float), [t, Xt, Rt, Xt1])
        At = np.array(At, dtype=np.int)
        loss = model.train_Xy(Xt, At, Rt, Xt1)

        with open(train_log_filename, 'a') as fp:
            fp.write('%d,%d,%f\n' % (episode, t.shape[0], loss))

if __name__ == '__main__':
    train()
