from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from chatbot.rag_pipeline import generate_answer

app = FastAPI()

# ✅ Allow frontend (GitHub Pages) to call backend (Render)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or replace "*" with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/chat")
def chat(query: str = Query(..., description="Your question")):
    answer = generate_answer(query)
    return {"question": query, "answer": answer}
