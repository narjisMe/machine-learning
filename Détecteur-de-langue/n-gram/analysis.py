import random
from collections import defaultdict


def compute_words_histogram(words: list[str]) -> list:
    hist = defaultdict(lambda: 0)
    for word in words:
        hist[word] += 1

    return sorted(hist.items(), key=lambda item: item[1], reverse=True)


def compute_ngrams_histogram(words: list[str], n: int, norm: bool = True) -> list:
    hist = defaultdict(lambda: 0)
    for i in range(len(words) - n + 1):
        ngram = " ".join(words[i:i + n])
        hist[ngram] += 1

    histogram = sorted(hist.items(), key=lambda item: item[1], reverse=True)
    if norm:
        total = sum(hist.values())
        histogram = [(ngram, count / total) for ngram, count in histogram]
    return histogram


def compute_next_word_probs(words: list[str]) -> dict[str, list[tuple[str, float]]]:
    n2grams = compute_ngrams_histogram(words, 2, norm=False)
    next_word_freqs = defaultdict(lambda: [])

    for ngram, count in n2grams:
        first, second = ngram.split()
        next_word_freqs[first].append((second, count))

    next_word_probs = {}
    for word, next_words in next_word_freqs.items():
        total_next = sum(count for _, count in next_words)
        next_word_probs[word] = [(next_word, count / total_next) for next_word, count in next_words]
    return next_word_probs


def draw_next_word(probs: list[tuple[str, float]]) -> str:
    words = [w for w, _ in probs]
    weights = [w for _, w in probs]
    next_word = random.choices(words, weights, k=1)
    return next_word[0]
