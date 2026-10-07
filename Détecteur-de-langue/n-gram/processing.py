import string


def split_by_words(text: str) -> list[str]:
    words = []
    for word in text.lower().split():
        for part in word.split("'"):
            part = part.strip(string.punctuation)
            if part:
                words.append(part)
    return words


if __name__ == "__main__":
    text = '''Le Poète est semblable au prince des nuées
Qui hante la tempête et se rit de l'archer;
Exilé sur le sol au milieu des huées,
Ses ailes de géant l'empêchent de marcher.

-- Charles Baudelaire'''
    words = split_by_words(text)
    print(words)
