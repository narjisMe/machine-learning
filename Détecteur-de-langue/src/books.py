import csv
import pathlib

from analysis import compute_character_histogram, histogram_distance, avg_hist
from visualization import save_character_histogram
from classifier import language_from_histogram

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

    all_hists = {}
    fr_hists = []
    en_hists = []
    for book in books:
        bookid, author, title, language = book
        book_file = cwd.parent / "data" / f"pg{book[0]}.txt"
        book_content = get_book_content(book_file)
        hist = compute_character_histogram(book_content)
        save_character_histogram(hist, title, cwd / f"char_histogram_{bookid}.png")
        all_hists[bookid] = hist
        if language == 'fr':
            fr_hists.append(hist)
        else:
            en_hists.append(hist)

        prediction = language_from_histogram(hist)
        print(title, "langue", language, "prediction", prediction)

    print("nb livres fr", len(fr_hists))
    print("nb livres en", len(en_hists))

    avg_fr_hist = avg_hist(fr_hists)
    avg_en_hist = avg_hist(en_hists)

    save_character_histogram(avg_fr_hist, "moyenne français", cwd / "avg_fr_hist.png")
    save_character_histogram(avg_en_hist, "moyenne anglais", cwd / "avg_en_hist.png")

    for bookid, author, title, language in books:
        hist = all_hists[bookid]
        distance_fr = histogram_distance(hist, avg_fr_hist)
        distance_en = histogram_distance(hist, avg_en_hist)
        if distance_fr < distance_en:
            prediction = "fr"
        else:
            prediction = "en"
        print(title)
        print("distance fr", distance_fr)
        print("distance en", distance_en)
        print("langue", language, "prediction", prediction)


if __name__ == "__main__":
    main()
