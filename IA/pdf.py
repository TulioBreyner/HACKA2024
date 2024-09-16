import pymupdf

def read_pdf(file):
    doc = pymupdf.open(file)
    return [page.get_text().lower() for page in doc]