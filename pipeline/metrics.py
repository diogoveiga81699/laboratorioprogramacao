def calculate_text_metrics(text):
    words = text.split()
    lines = text.splitlines()
    characters = len(text)

    empty_lines = sum(1 for line in lines if not line.strip())

    return {
        "characters": characters,
        "words": len(words),
        "lines": len(lines),
        "empty_lines": empty_lines
    }


def compare_metrics(raw_text, cleaned_text):
    raw = calculate_text_metrics(raw_text)
    cleaned = calculate_text_metrics(cleaned_text)

    return {
        "raw": raw,
        "cleaned": cleaned,
        "characters_removed": raw["characters"] - cleaned["characters"],
        "empty_lines_removed": raw["empty_lines"] - cleaned["empty_lines"]
    }