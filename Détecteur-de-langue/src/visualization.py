import string
import pathlib

from matplotlib import pyplot as plt
from analysis import HistDict


def plot_character_histogram(hist_norm: HistDict,
                             booktitle: str) -> plt.Figure:
    chars = [k for k in string.ascii_lowercase]
    counts = []
    for key in chars:
        counts.append(hist_norm[key])
    fig = plt.figure()
    plt.bar(chars, counts)
    plt.title(booktitle)
    return fig


def save_character_histogram(hist: HistDict, booktitle: str,
                             filename: pathlib.Path):
    fig = plot_character_histogram(hist, booktitle)
    fig.savefig(filename)
    plt.close(fig)
