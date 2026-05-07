from langdetect import detect, LangDetectException


def detect_language(text):
    try:
        language = detect(text)

        language_map = {
            "pt": "Português",
            "en": "Inglês",
            "es": "Espanhol",
            "fr": "Francês"
        }

        return language_map.get(language, language)
    except LangDetectException:
        return "Idioma não detetado"