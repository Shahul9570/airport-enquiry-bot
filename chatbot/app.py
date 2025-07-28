# chatbot/app.py
from fastapi import FastAPI, Query
from chatbot.rag_pipeline import generate_answer

app = FastAPI()

@app.get("/chat")
def chat(query: str = Query(..., description="Your question")):
    answer = generate_answer(query)
    return {"question": query, "answer": answer}
@app.get("/")
def home():
    return {"message": "Welcome to the Airport Enquiry Bot API! Use /chat?query=your_question"}

