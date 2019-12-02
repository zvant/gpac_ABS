#!python3

import csv
import numpy as np
import matplotlib.pyplot as plt


def plot():
    bitrates = [776, 971, 1944, 2724]
    colors = ['#E8FA5BBB', '#F68F46BB', '#A65C85BB', '#403891BB']
    alphas = [0.0, 0.5, 0.9, 1.0]

    plt.figure(figsize=(12, 9))
    for loss_i in range(0, 3):
        loss = [0, 6, 16][loss_i]
        plt.subplot(3, 1, loss_i + 1)
        plt.title('$\\lambda=%d\\%%$' % loss)

        for alpha_i in range(0, 4):
            alpha = alphas[alpha_i]
            with open('%d_%.1f.csv' % (loss, alpha), 'r') as fp:
                csvreader = csv.reader(fp, delimiter=',')
                segs = np.array(list(csvreader))
                segs = segs[:, 0:2].astype(np.int)
                for idx in range(0, segs.shape[0]):
                    segs[idx, 1] = bitrates[segs[idx, 1]]
                    segs[idx, 0] += 1
            plt.plot(segs[:, 0], segs[:, 1], color=colors[alpha_i], lw=2)
        plt.legend(list(map(lambda a: '$\\alpha=%.1f$' % a, alphas)), loc='upper right')
        plt.ylabel('bitrate (kbps)')
        plt.ylim([0, 3000])
        plt.xticks(range(1, 21))

    plt.xlabel('# chunks')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    plot()
