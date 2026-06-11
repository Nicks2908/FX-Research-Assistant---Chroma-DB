import google.generativeai as genai

def generate_embedding(text):

    result = genai.embed_content(model="models/gemini-embedding-001", content=text)
    return result["embedding"]