import re
import unicodedata
from collections import Counter


def normalize_unicode(text):
    return unicodedata.normalize("NFKC", text)


def remove_invalid_chars(text):
    return re.sub(r"[^\x09\x0A\x0D\x20-\x7EÀ-ÿ€ºªçÇ“”‘’«»—–…]", "", text)


def normalize_spaces(text):
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def fix_broken_lines(text):
    lines = text.splitlines()
    rebuilt = []

    for line in lines:
        stripped = line.strip()

        if not stripped:
            rebuilt.append("")
            continue

        if rebuilt and rebuilt[-1] and not rebuilt[-1].endswith((".", "!", "?", ":", ";")):
            rebuilt[-1] += " " + stripped
        else:
            rebuilt.append(stripped)

    return "\n".join(rebuilt)


def normalize_punctuation(text):
    text = text.replace(" ,", ",")
    text = text.replace(" .", ".")
    text = text.replace(" ;", ";")
    text = text.replace(" :", ":")
    text = text.replace(" !", "!")
    text = text.replace(" ?", "?")
    return text


def remove_repeated_headers_footers(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    counter = Counter(lines)

    repeated_lines = {
        line for line, count in counter.items()
        if count >= 3 and len(line) < 100
    }

    cleaned_lines = [
        line for line in text.splitlines()
        if line.strip() not in repeated_lines
    ]

    return "\n".join(cleaned_lines)


def clean_text(
    text,
    remove_artifacts=True,
    rebuild_paragraphs=True,
    normalize_spacing=True,
    normalize_punct=True,
    remove_headers=True
):
    steps_applied = []
    cleaned = text

    if remove_artifacts:
        cleaned = normalize_unicode(cleaned)
        cleaned = remove_invalid_chars(cleaned)
        steps_applied.append("Remoção de artefactos e normalização Unicode")

    if remove_headers:
        cleaned = remove_repeated_headers_footers(cleaned)
        steps_applied.append("Remoção de cabeçalhos/rodapés repetidos")

    if rebuild_paragraphs:
        cleaned = fix_broken_lines(cleaned)
        steps_applied.append("Reconstrução de parágrafos")

    if normalize_spacing:
        cleaned = normalize_spaces(cleaned)
        steps_applied.append("Normalização de espaços e quebras de linha")

    if normalize_punct:
        cleaned = normalize_punctuation(cleaned)
        steps_applied.append("Normalização de pontuação")

    return cleaned, steps_applied
