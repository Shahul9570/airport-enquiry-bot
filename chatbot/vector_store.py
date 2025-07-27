# chatbot/vector_store.py
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

load_dotenv()

# Load env vars
api_key = os.getenv("PINECONE_API_KEY")
env = os.getenv("PINECONE_ENV")         # e.g., "gcp-starter"
index_name = os.getenv("PINECONE_INDEX")
dimension = 384                         # SentenceTransformer: all-MiniLM-L6-v2

# Connect to Pinecone
pc = Pinecone(api_key=api_key)

# Create index if not exists
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=dimension,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",          # or "gcp"
            region=env            # e.g., "us-west-1"
        )
    )

# Load index
index = pc.Index(index_name)

embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def upload_embeddings(docs):
    vectors = []
    for i, doc in enumerate(docs):
        emb = embed_model.encode(doc).tolist()
        vectors.append({"id": f"id-{i}", "values": emb, "metadata": {"text": doc}})
    index.upsert(vectors)
