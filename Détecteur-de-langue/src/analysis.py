import string
from collections import defaultdict

type HistDict = dict[str, float]


def compute_character_histogram(book_content: str) -> HistDict:
    hist = defaultdict(lambda: 0)
    for c in string.ascii_lowercase:
        hist[c] = 0

    for c in book_content.lower():
        if c in string.ascii_lowercase:
            hist[c] += 1

    nb_caracteres = sum(hist.values())
    hist_norm: HistDict = {}
    for key, val in hist.items():
        hist_norm[key] = val / nb_caracteres
    return hist_norm


def histogram_distance(h0: HistDict, h1: HistDict) -> float:
    distance = 0
    for o in range(ord('a'), ord('z') + 1):
        c = chr(o)
        distance += abs(h0.get(c, 0) - h1.get(c, 0))
    return distance


def avg_hist(hists: list[HistDict]) -> HistDict:
    avg: HistDict = {}
    for hist in hists:
        for key, val in hist.items():
            if key not in avg:
                avg[key] = 0
            avg[key] += val
    total = sum(val for val in avg.values())
    avg = {key: val / total for key, val in avg.items()}
    return avg
