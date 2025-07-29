# app.py

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from chatbot.rag_pipeline import generate_answer

app = FastAPI()

# Allow GitHub Pages origin only (not "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://shahul9570.github.io"],  # ✅ NOT "*"
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
    return {"question": query, "answer": generate_answer(query)}


