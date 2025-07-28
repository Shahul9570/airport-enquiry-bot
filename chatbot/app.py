from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from chatbot.rag_pipeline import generate_answer

app = FastAPI()

# Allow cross-origin for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Changi Airport Chatbot API is running!"}

@app.get("/chat")
def chat(query: str = Query(..., description="Your question")):
    answer = generate_answer(query)
    return {"question": query, "answer": answer}
