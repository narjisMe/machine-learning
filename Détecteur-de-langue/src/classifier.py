from analysis import HistDict


def language_from_histogram(hist: HistDict) -> str:

    if hist['h'] > 0.03:
        return "en"
    else:
        return "fr"
