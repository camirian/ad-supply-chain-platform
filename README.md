# A&D Supply Chain AI Agent

An enterprise-grade platform demonstrating an Aerospace & Defense supply chain conversational agent. 
This project leverages a LangChain text-to-SQL architecture to query a relational SQLite database using natural language. It boasts a fully decoupled V2 architecture consisting of a **FastAPI** backend and a **Vite React** frontend natively structured for zero-billing Cloud Run deployments.

> **Traceability**: This project specifically fulfills the following Enterprise IT and Applied AI capabilities from my portfolio:
> *   **CPS_CAP_05**: A&D Supply Chain AI Agent (Full-stack MVP utilizing LangChain and Google Gemini)
> *   **CPS_NAV_01**: Architected the Shop Workload Management System for depot production control, leveraging relational database systems

> **Breadcrumb Protocol**
> *   [🚀 QUICKSTART: Deploying this Template](DEPLOY.md)
> *   [🏗️ READ: Architectural Architecture](docs/ARCHITECTURE.md)

## Features
- **Relational Backend**: A normalized `SQLite` database modeling typical A&D supply chain entities (Parts, Suppliers, Work Orders), suitable for ephemeral container execution.
- **Conversational RAG / NLP Agent**: Natural language to SQL translation using `LangChain` and **Google Gemini 1.5-Flash** (`langchain-google-genai`).
- **Premium Frontend**: An accessible and highly aesthetic React web application providing a dynamic chat interface and schema parsing.
- **Zero-Billing**: Configured explicitly for Google Cloud Run scale-to-zero serverless environments.

## Local Quickstart 

### Installation
1. Install Python dependencies and initialize the SQLite seed:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python backend/db_init.py
export GOOGLE_API_KEY="your-gemini-key-here"
```

2. Start the Backend API:
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

3. Install Node dependencies and start the React app:
```bash
cd web
npm install
npm run dev
```

Navigate to `http://localhost:5173` to query the agent!
