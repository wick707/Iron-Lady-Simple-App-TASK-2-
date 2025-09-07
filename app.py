"""
Iron Lady RAG Chatbot
Version 8.1 (Final): Multi-mode support (FAQ & Recommendations) with clean file serving.
"""

import os
import re
import pickle
import threading
import time
import requests
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from dotenv import load_dotenv

# ----------------- Load config -----------------
load_dotenv()

KB_FILENAME = os.getenv("KB_FILE", "knowledgebase.md")
INDEX_PATH = "vector_index.faiss"
META_PATH = "vector_meta.pkl"
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

TOP_K = int(os.getenv("TOP_K", 8))
MAX_HISTORY_TURNS = int(os.getenv("MAX_HISTORY_TURNS", 8))

# Groq config
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEN_MODEL_NAME = os.getenv("GEN_MODEL", "llama-3.1-8b-instant")

# ----------------- Globals -----------------
emb_model: Optional[SentenceTransformer] = None
index = None
chunks: List[str] = []

# ----------------- Helper Functions -----------------

def clean_text(raw: str) -> str:
    raw = re.sub(r"\s+\n", "\n", raw)
    raw = re.sub(r"\n{3,}", "\n\n", raw)
    raw = re.sub(r" {2,}", " ", raw)
    return raw.strip()

def read_markdown_file(path: str) -> str:
    if not os.path.exists(path):
        return f"Knowledge base file missing: {path}"
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return clean_text(f.read())
    except Exception as e:
        print(f"Error reading file {path}: {e}")
        return ""

def chunk_text(text: str, separator: str = "\n---\n") -> List[str]:
    chunks_list = text.split(separator)
    return [chunk.strip() for chunk in chunks_list if chunk.strip()]

def get_embedding_model():
    global emb_model
    if emb_model is None:
        emb_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return emb_model

def build_or_load_index(force_rebuild: bool = False):
    global index, chunks
    kb_mtime = os.path.getmtime(KB_FILENAME) if os.path.exists(KB_FILENAME) else None
    if not force_rebuild and os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
        with open(META_PATH, "rb") as f:
            meta = pickle.load(f)
        if meta.get("kb_mtime") == kb_mtime:
            index = faiss.read_index(INDEX_PATH)
            chunks = meta["chunks"]
            print(f"Loaded existing index. {len(chunks)} chunks.")
            return

    print("Rebuilding index...")
    text = read_markdown_file(KB_FILENAME)
    chunks = chunk_text(text)
    print(f"Index rebuild in progress for {len(chunks)} chunks.")
    model = get_embedding_model()
    emb = model.encode(chunks, convert_to_numpy=True, normalize_embeddings=True)
    faiss_index = faiss.IndexFlatIP(emb.shape[1])
    faiss_index.add(emb.astype(np.float32))
    faiss.write_index(faiss_index, INDEX_PATH)
    index = faiss_index
    with open(META_PATH, "wb") as f:
        pickle.dump({"chunks": chunks, "kb_mtime": kb_mtime}, f)
    print("Index data saved.")

def search_similar(query: str, k: int) -> List[Dict[str, Any]]:
    model = get_embedding_model()
    q = model.encode([query], convert_to_numpy=True, normalize_embeddings=True).astype(np.float32)
    k_safe = min(k, len(chunks))
    if k_safe == 0: return []
    D, I = index.search(q, k_safe)
    return [{"score": float(score), "chunk": chunks[idx], "id": int(idx)} for score, idx in zip(D[0], I[0])]

def generate_answer(prompt: str) -> str:
    if not GROQ_API_KEY: return "Error: GROQ_API_KEY not set."
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": GEN_MODEL_NAME, "messages": [{"role": "user", "content": prompt}], "temperature": 0.3, "max_tokens": 2000}
    max_retries = 3
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"].strip()
            elif resp.status_code == 429:
                time.sleep(1 * (2 ** attempt))
            else:
                resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1: return f"API Error: {e}"
            time.sleep(1 * (2 ** attempt))
    return "API Error: Failed after multiple retries."

# ----------------- Prompt Engineering (Multi-Prompt) -----------------

def build_faq_prompt(question: str, context_str: str, history_str: str) -> str:
    return f"""You are "Iron Lady Bot," a highly precise FAQ assistant.
**Core Instructions:**
1.  **Analyze Intent:** Determine the specific topic the user is asking about (e.g., duration, cost, mode, mentors, or a general overview).
2.  **Targeted Extraction:** Scan the "Retrieved Context" to find information related *only* to that topic for all three core programs.
3.  **Concise Answer Generation:** Present the findings clearly and concisely. Do not add extra information that was not requested.
    * **Exception:** If the user asks a general question like "what programs do you offer?", then provide a full summary.
    * **Missing Data:** If the context lacks the specific attribute, state: "Details for [Program Name] regarding this topic are not available."
---BEGIN RETRIEVED CONTEXT---
{context_str}
---END RETRIEVED CONTEXT---
---BEGIN CHAT HISTORY---
{history_str}---END CHAT HISTORY---
**User Question:** {question}
**Answer (concise and specific to the user's question topic):**
"""

def build_recommend_prompt(question: str, context_str: str, history_str: str) -> str:
    return f"""You are "Iron Lady Bot," a helpful career program advisor.
**Your Goal:** Guide the user to the best program for their needs based on their input and the "Interests Aligned" section in the context.
**Workflow:**
1.  **Check for User Input:** Read the user's latest message. Have they described their career, goals, or interests?
2.  **If Input is Missing:** Your first response MUST be to ask for more information. Ask a question like, "To recommend the best course for you, could you please tell me a bit about your professional background, your career goals, or any specific interests you have?" Do not recommend a course yet.
3.  **If Input is Provided:** Analyze the user's message (e.g., "I am a software developer," "I want to join a board"). Compare their input to the "Interests Aligned" section for each program in the "Retrieved Context".
4.  **Make a Recommendation:** Recommend the SINGLE best program that matches their interests. Clearly state the program name and explain *why* it's a good fit by referencing their input and the aligned interests from the context.
---BEGIN RETRIEVED CONTEXT---
{context_str}
---END RETRIEVED CONTEXT---
---BEGIN CHAT HISTORY---
{history_str}---END CHAT HISTORY---
**User Question:** {question}
**Advisor's Response:**
"""

# ----------------- FastAPI Application Setup -----------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup...")
    get_embedding_model()
    build_or_load_index()
    print("Application ready.")
    yield
    print("Application shutting down.")

app = FastAPI(title="Iron Lady Advisor", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = []
    mode: str = "faq"

@app.get("/", response_class=FileResponse)
def read_root():
    return "index.html"

@app.get("/chatbot", response_class=FileResponse)
def read_chatbot_ui():
    return "chatbot.html"

@app.post("/chat")
def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")

    retrieved = search_similar(req.message, k=TOP_K)
    context_str = "\n\n---\n\n".join([r["chunk"] for r in retrieved])
    history_str = "".join([f"User: {turn.get('user', '')}\nAssistant: {turn.get('assistant', '')}\n" for turn in req.history])

    if req.mode == "recommend":
        prompt = build_recommend_prompt(req.message, context_str, history_str)
    else:
        prompt = build_faq_prompt(req.message, context_str, history_str)

    answer = generate_answer(prompt)

    return JSONResponse({
        "answer": answer,
        "sources": [{"id": r["id"], "score": r["score"]} for r in retrieved]
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")), reload=False)

