from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os

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
        # Check for fake key explicitly to mimic the old system warning
        if os.environ.get("GOOGLE_API_KEY") == "fake-key-for-testing" or not os.environ.get("GOOGLE_API_KEY"):
            return ChatResponse(response=f"[Simulated Response]: You asked '{request.prompt}'. Please provide a GOOGLE_API_KEY to execute.")
            
        answer = query_agent(request.prompt)
        return ChatResponse(response=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
