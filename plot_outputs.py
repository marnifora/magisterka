import matplotlib.pyplot as plt
import argparse
import os
import numpy as np
from bin.common import *

COLORS = ['C{}'.format(i) for i in range(10)]

parser = argparse.ArgumentParser(description='Plot results based on given table')
parser.add_argument('-f', '--file', action='store', metavar='NAME', type=str, default=None, nargs='+',
                    help='Files with the outputs to plot, if PATH is given, file is supposed to be '
                         'in PATH directory: [PATH]/[NAME], default: [PATH]/[NAMESPACE]_valid_outputs.npy')
group1 = parser.add_mutually_exclusive_group(required=False)
group1.add_argument('--train', action='store_true',
                    help='Use values from training, default values from validation are used')
group1.add_argument('--test', action='store_true',
                    help='Use testing results.')
parser = basic_params(parser, param=True)
args = parser.parse_args()

path, output, namespace, seed = parse_arguments(args, args.file, model_path=True)
if args.file:
    if args.path is not None:
        file = os.path.join(path, args.file)
    else:
        file = args.file
    stage = 'all'
else:
    if args.test:
        stage = 'test'
    elif args.train:
        stage = 'train'
    else:
        stage = 'valid'
    file = os.path.join(path, '{}_{}_outputs.npy'.format(namespace, stage))
if not os.path.isfile(file):
    file = os.path.join(path, namespace + '_outputs.tsv')

neurons = get_classes_names(os.path.join(path, '{}_params.txt'.format(namespace)))


def set_box_color(box, color):
    for el in box.keys():
        plt.setp(box[el], color=color)


fig, axes = plt.subplots(nrows=len(neurons), ncols=1, figsize=(10, 15), squeeze=True)
colors = COLORS[:len(neurons)]
values = np.load(file, allow_pickle=True)
for j, (row, ax, name) in enumerate(zip(values, axes, neurons)):
    if row.any():
        for i, m in enumerate(row):
            box = ax.boxplot(m, positions=[i+1], widths=[0.4], sym='.')
            set_box_color(box, colors[i])
    else:
        ax.plot([])
    ax.set_ylabel(name.replace(' ', '\n'), color=colors[j], rotation=0, horizontalalignment='right', fontsize=8)
    ax.yaxis.set_label_coords(-0.06, 0.45)
    ax.set_xticks([])
    ax.tick_params(size=3)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlim(0.0, len(neurons)+1.0)
    plt.setp(ax.get_yticklabels(), fontsize=8)

fig.suptitle('{} - {} data'.format(namespace, STAGES[stage]), fontsize=12)
plt.xticks([i+1 for i in range(len(neurons))], neurons, fontsize=8)
for ticklabel, tickcolor in zip(plt.gca().get_xticklabels(), colors):
    ticklabel.set_color(tickcolor)
ax = fig.add_subplot(111, frameon=False)
ax.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off', axis=u'both', which=u'both', length=0)
ax.grid(False)
ax.set_ylabel("Real labels", fontsize=12)
ax.set_title('Neurons', fontsize=12)
ax.yaxis.set_label_coords(-0.12, 0.5)
plt.savefig(os.path.join(output, '{}_{}_outputs.png'.format(namespace, stage)))
plt.show()
