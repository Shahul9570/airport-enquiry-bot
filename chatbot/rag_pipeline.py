# chatbot/rag_pipeline.py

import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from huggingface_hub import InferenceClient
import pinecone


# Load environment variables
load_dotenv()

# Hugging Face inference client for flan-t5-base (hosted, free)
client = InferenceClient("google/flan-t5-base")

# Pinecone setup
api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX")
pinecone.init(api_key=api_key)
index = pinecone.Index(index_name)

# Sentence embedding model
embed_model = SentenceTransformer('paraphrase-MiniLM-L3-v2')



# Step 1: Embed the user query
def get_query_embedding(query):
    return embed_model.encode(query).tolist()


# Step 2: Search Pinecone for relevant content
def retrieve_documents(query, top_k=5):
    query_vector = get_query_embedding(query)
    results = index.query(vector=query_vector, top_k=top_k, include_metadata=True)
    docs = [match['metadata']['text'] for match in results['matches']]
    return docs


# Step 3: Generate answer using hosted flan-t5-base model
def generate_answer(query):
    try:
        print("🔍 Query:", query)
        documents = retrieve_documents(query)
        print("📄 Retrieved:", documents)

        if not documents:
            return "No relevant information found."

        context = "\n".join(documents)
        prompt = f"""Use the context below to answer the question. If the answer is not found, say "I don't know."

Context:
{context}

Question: {query}
Answer:"""

        print("🤖 Sending prompt to Hugging Face Inference API...")
        response = client.text_generation(prompt, max_new_tokens=150)
        print("✅ Response received")
        return response.strip()

    except Exception as e:
        import traceback
        print("❌ Full Error Trace:")
        traceback.print_exc()
        return "An error occurred."
