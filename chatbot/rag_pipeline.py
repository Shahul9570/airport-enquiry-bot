# chatbot/rag_pipeline.py

import os
from dotenv import load_dotenv
import pinecone
from sentence_transformers import SentenceTransformer
from transformers import pipeline

qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-base", max_new_tokens=256)

# Load Hugging Face text generation pipeline

load_dotenv()

# Initialize APIs


from pinecone import Pinecone

# Load keys
api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX")

# Connect
pc = Pinecone(api_key=api_key)
index = pc.Index(index_name)

embed_model = SentenceTransformer('all-MiniLM-L6-v2')


# Step 1: Embed the user query
def get_query_embedding(query):
    return embed_model.encode(query).tolist()

# Step 2: Search Pinecone for relevant content
def retrieve_documents(query, top_k=5):
    query_vector = get_query_embedding(query)
    results = index.query(vector=query_vector, top_k=top_k, include_metadata=True)
    docs = [match['metadata']['text'] for match in results['matches']]
    return docs

# Step 3: Send context + query to OpenAI to generate an answer
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

        print("🤖 Sending prompt to Hugging Face model...")
        output = qa_pipeline(prompt)[0]["generated_text"]
        print("✅ Response received")

        # Extract only the final answer
        return output.split("Answer:")[-1].strip()

    except Exception as e:
        import traceback
        print("❌ Full Error Trace:")
        traceback.print_exc()
        return "An error occurred."



# Test it directly
if __name__ == "__main__":
    while True:
        user_query = input("\nAsk a question (type 'exit' to quit): ")
        if user_query.lower() == 'exit':
            break
        answer = generate_answer(user_query)
        print("\n🧠 Answer:", answer)
