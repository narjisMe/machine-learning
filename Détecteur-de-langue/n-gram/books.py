import csv
import pathlib

from processing import split_by_words
from analysis import compute_words_histogram, compute_ngrams_histogram
from analysis import compute_next_word_probs, draw_next_word


def get_books(csv_file: pathlib.Path) -> list:
    with csv_file.open('r', encoding='utf-8') as fp:
        reader = csv.reader(fp, delimiter=';')
        next(reader)
        data = [row for row in reader]
    return data


def get_book_content(book_file: pathlib.Path) -> str:
    with book_file.open('r', encoding='utf-8') as fp:
        txt = fp.read()
        start = txt.find('*** START')
        start = txt.find('\n', start) + 1
        end = txt.find('*** END', start)
    return txt[start:end]


def main():
    cwd = pathlib.Path(__file__).parent
    books = get_books(cwd.parent / "data" / "books.csv")
    french_text = ""

    for book in books:
        bookid, author, title, language = book
        book_file = cwd.parent / "data" / f"pg{bookid}.txt"
        book_content = get_book_content(book_file)
        words = split_by_words(book_content)

        hist = compute_words_histogram(words)
        n2grams = compute_ngrams_histogram(words, 2, norm=False)
        n3grams = compute_ngrams_histogram(words, 3, norm=False)

        print(title)
        print("top 5 mots", hist[:5])
        print("top 5 2-grams", n2grams[:5])
        print("top 5 3-grams", n3grams[:5])
        print()

        if language == 'fr':
            french_text += book_content + " "

    words = split_by_words(french_text)
    next_word_probs = compute_next_word_probs(words)
    word = "le"
    generated_words = [word]

    for i in range(49):
        if word not in next_word_probs:
            break
        word = draw_next_word(next_word_probs[word])
        generated_words.append(word)

    print("texte genere")
    print(" ".join(generated_words))


if __name__ == "__main__":
    main()
