# app.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://shahul9570.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Changi Airport Chatbot API is running!"}

from chatbot.rag_pipeline import generate_answer

@app.get("/chat")
def chat(query: str = Query(...)):
    answer = generate_answer(query)
    return {"question": query, "answer": answer}

