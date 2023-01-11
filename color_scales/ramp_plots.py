from matplotlib import pyplot as plt
import numpy as np

import colour


def plot_ramps(ramps):
    for i, name in enumerate(ramps):
        hsv = ramps[name]
        for k in range(len(ramps[name])):
            plt.fill_between(
                [k, k + 1],
                [i - 0.5] * 2,
                [i + 0.5] * 2,
                color=colour.HSV_to_RGB(hsv[k]),
            )
    plt.xlim(len(ramps[name]), 0)
    plt.ylim(len(ramps) - 0.5, -0.5)
    plt.yticks(np.arange(len(ramps)), list(ramps))
