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

@app.get("/chat")
def chat(query: str = Query(..., description="Your question")):
    try:
        answer = generate_answer(query)
        return {"question": query, "answer": answer}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e), "message": "Chatbot failed to generate a response"}

