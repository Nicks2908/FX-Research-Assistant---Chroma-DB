
def create_chunks(pages, chunk_size=1000, overlap=200):
    chunks = []
    for page in pages:
        text = page["text"]
        page_no = page["page_no"]
        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))
            # chunk = text[start:end]
            # chunks.append(chunk)
            chunks.append(
                {
                    "page_no": page_no,
                    "text": text[start:end]
                }
            )  # Include page number in the chunk

            start += chunk_size - overlap
    return chunks














