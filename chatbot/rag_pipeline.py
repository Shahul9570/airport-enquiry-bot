# chatbot/rag_pipeline.py

import os
from dotenv import load_dotenv
import pinecone
from sentence_transformers import SentenceTransformer
import requests

# Load environment variables
load_dotenv()

# Hugging Face Token from Render environment
HF_API_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Pinecone setup
api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX")

# Initialize Pinecone client
pinecone.init(api_key=api_key)
index = pinecone.Index(index_name)

# Load embedding model
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# Hugging Face generation call
def generate_answer_from_huggingface(prompt):
    response = requests.post(
        "https://api-inference.huggingface.co/models/google/flan-t5-small",
        headers={"Authorization": f"Bearer {HF_API_TOKEN}"},
        json={"inputs": prompt},
    )
    result = response.json()
    return result[0]["generated_text"]

# Step 1: Get query embedding
def get_query_embedding(query):
    return embed_model.encode(query).tolist()

# Step 2: Retrieve relevant documents
def retrieve_documents(query, top_k=5):
    query_vector = get_query_embedding(query)
    results = index.query(vector=query_vector, top_k=top_k, include_metadata=True)
    docs = [match['metadata']['text'] for match in results['matches']]
    return docs

# Step 3: Generate answer using context
def generate_answer(query):
    try:
        print("🔍 Query:", query)
        documents = retrieve_documents(query)
        print("📄 Retrieved:", documents)

        if not documents:
            return "No relevant information found."

        context = "\n".join(documents)
        prompt = f"""
Use the context below to answer the question. If the answer is not found, say "I don't know."

Context:
{context}

Question: {query}
Answer:"""

        print("🤖 Sending prompt to Hugging Face...")
        output = generate_answer_from_huggingface(prompt)
        print("✅ Response received")

        return output.split("Answer:")[-1].strip()

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Error: {e}"

# Optional: Local testing
if __name__ == "__main__":
    while True:
        user_query = input("\nAsk a question (type 'exit' to quit): ")
        if user_query.lower() == 'exit':
            break
        answer = generate_answer(user_query)
        print("\n🧠 Answer:", answer)
