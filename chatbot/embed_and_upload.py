# chatbot/embed_and_upload.py

from chatbot.vector_store import upload_embeddings
from chatbot.utils import split_text

def load_and_prepare_text():
    with open("data/combined_text.txt", "r", encoding="utf-8") as f:
        raw_text = f.read()
    return split_text(raw_text)

if __name__ == "__main__":
    docs = load_and_prepare_text()
    print("Uploading", len(docs), "chunks to Pinecone...")
    upload_embeddings(docs)
