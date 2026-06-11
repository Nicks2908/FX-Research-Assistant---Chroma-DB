import chromadb

# client = chromadb.PersistentClient(
#     path="./chroma_db"
# )

client = chromadb.EphemeralClient()

collection = client.get_or_create_collection(
    name="forex_reports"
)

def store_chunks(chunks, embeddings):

    ids = []
    documents = []
    metadatas = []

    for idx, chunk in enumerate(chunks):

        ids.append(str(idx))
        # ids.append(idx)
        documents.append(chunk["text"])

        metadatas.append(
            {
                "document": chunk["document"],
                "page": chunk["page_no"]
            }
        )

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

def search_chunks(query_embedding, k=3):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results