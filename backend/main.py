from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import os

import logging
logging.basicConfig(level=logging.DEBUG)
import langchain
langchain.debug = True

from rag.nlp_agent import query_agent

app = FastAPI(
    title="A&D Supply Chain Agent API",
    description="Backend API for the Agentic Supply Chain platform.",
    version="2.0.0"
)

# Standard CORS setup for modern decoupled architecture
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt: str
    api_key: str | None = None

class ChatResponse(BaseModel):
    response: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Accepts a natural language prompt and returns the result from the text-to-SQL logic block.
    """
    try:
        # Ensure we have a valid key to use
        key_to_use = request.api_key or os.environ.get("GOOGLE_API_KEY")
        
        if key_to_use in ["fake-key-for-testing", None, ""]:
            return ChatResponse(response=f"[Simulated Response]: You asked '{request.prompt}'. Please provide a valid GOOGLE_API_KEY to execute.")
            
        answer = query_agent(request.prompt, api_key=key_to_use)
        return ChatResponse(response=answer)
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "not found" in error_msg.lower():
            try:
                import urllib.request
                import json
                req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models?key={key_to_use}")
                with urllib.request.urlopen(req) as response:
                    models_data = json.loads(response.read().decode())
                    available_models = [m['name'] for m in models_data.get('models', []) if 'generateContent' in m.get('supportedGenerationMethods', [])]
                    return ChatResponse(
                        response=f"**Model Error Identified.** The requested model was not found.\n\nHere are the models your API key actually has access to:\n" + 
                                 "\n".join([f"- `{m}`" for m in available_models]) +
                                 "\n\nPlease update `rag/nlp_agent.py` to use one of these models specifically."
                    )
            except Exception as inner_e:
                error_msg += f"\n\n(Also failed to fetch models list: {inner_e})"
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/api/docs")
def list_docs():
    """Returns a list of available documentation files."""
    return {"docs": ["README.md", "DEPLOY.md", "docs/ARCHITECTURE.md"]}

@app.get("/api/docs/{doc_id:path}")
def get_doc(doc_id: str):
    """Fetches a specific documentation file."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target = os.path.abspath(os.path.join(base_dir, doc_id))
    
    # Security: prevent directory traversal
    if not target.startswith(base_dir):
        raise HTTPException(status_code=403, detail="Invalid path")
    if not os.path.exists(target):
        raise HTTPException(status_code=404, detail="Document not found")
        
    with open(target, 'r') as f:
        content = f.read()
    return {"content": content}

@app.get("/api/schema")
def get_schema():
    """
    Returns a brief snapshot of the SQLite database tables and mock data rows for the frontend UI.
    """
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'supply_chain.db')
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        tables = ['Suppliers', 'Parts', 'WorkOrders']
        schema_data = {}
        
        for table in tables:
            cur.execute(f"SELECT * FROM {table} LIMIT 5")
            rows = [dict(row) for row in cur.fetchall()]
            schema_data[table] = rows
            
        conn.close()
        return {"schema": schema_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
