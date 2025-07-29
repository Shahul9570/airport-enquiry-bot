# ✈️ Airport Enquiry Bot

An AI-powered chatbot that answers user queries about Changi Airport using Retrieval-Augmented Generation (RAG). This project integrates a FastAPI backend and a Streamlit frontend for both API and user-friendly interface support.

---



---

## 📁 Project Structure

```
airport-enquiry-bot/
                      
├── chatbot/
│   ├── app.py                 # FastAPI app wrapper (not root)
│   ├── crawl_urls.py          # Web crawler for Changi Airport URLs
│   ├── embed_and_upload.py    # Embed documents and upload to Pinecone
│   ├── rag_pipeline.py        # Core RAG pipeline
│   ├── scrape_changi.py       # HTML scraper for airport content
│   ├── utils.py               # Helper functions
│   └── vector_store.py        # Vector DB (Pinecone) handling
├── chatui.py           # Streamlit-based chatbot UI
├── requirements.txt           # Project dependencies
├── .env                       # Environment variables (not committed)
├── README.md                  # Project documentation
```

---

## ⚙️ Technology Stack

* **FastAPI**: API backend
* **Streamlit**: Web UI
* **Sentence Transformers**: Embedding text
* **Pinecone**: Vector database for document retrieval
* **Hugging Face Inference API**: Text generation

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Shahul9570/airport-enquiry-bot.git
cd airport-enquiry-bot
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

Create a `.env` file in the root with the following:

```
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX=your_index_name
HUGGINGFACE_TOKEN=your_huggingface_token
```

---

## 💡 How It Works

1. User enters a question via Streamlit or API.
2. Question is embedded using SentenceTransformer.
3. Pinecone retrieves top matching documents.
4. Context and question are sent to HuggingFace model.
5. Final answer is returned.

---


## 📲 Run Locally

### FastAPI

```bash
uvicorn app:app --reload
```

Visit: [http://localhost:8000](http://localhost:8000)

### Streamlit

```bash
streamlit run chatui.py
```

Visit: [http://localhost:8501](http://localhost:8501)

---

## 📢 Contact

For queries or collaboration, connect with [Muhammed Shahul](https://www.linkedin.com/in/muhammedshahul).
