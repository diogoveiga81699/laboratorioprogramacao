import pdfplumber


def extract_text_from_pdf(file):
    text = ""

    with pdfplumber.open(file) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text() or ""
            text += f"\n--- Página {page_number} ---\n"
            text += page_text

    return text