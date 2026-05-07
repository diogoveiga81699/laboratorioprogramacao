from docx import Document


def extract_text_from_docx(file):
    document = Document(file)
    paragraphs = []

    for paragraph in document.paragraphs:
        paragraphs.append(paragraph.text)

    return "\n".join(paragraphs)