def extract_text_from_txt(file):
    try:
        return file.read().decode("utf-8")
    except UnicodeDecodeError:
        file.seek(0)
        return file.read().decode("latin-1", errors="replace")