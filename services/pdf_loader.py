from pypdf import PdfReader

def extract_pages(file_path):
    reader = PdfReader(file_path)
    text = ""
    pages = []
    for page_no, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages.append(
                {
                    "page_no": page_no + 1,  # Page numbers are 1-indexed
                    "text": text
                }
            )
    return pages