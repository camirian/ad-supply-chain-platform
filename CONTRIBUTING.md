# Contributing to A&D Supply Chain Platform

We welcome contributions to the Aerospace & Defense Supply Chain Platform! To ensure the integrity of the text-to-SQL agent architecture, please adhere to the following guidelines.

## 🏗️ Architectural Constraints
1.  **Schema Awareness:** Any new database tables added to `backend/db_init.py` must follow the existing normalization conventions. LangChain's `SQLDatabase` introspects the schema automatically — poorly designed tables will degrade the agent's SQL generation quality.
2.  **SQL Sanitization:** All LLM-generated SQL must pass through the `clean_sql()` function in `rag/nlp_agent.py` before execution. Never execute raw LLM output directly against SQLite.
3.  **Zero-Billing Mandate:** This project is deployed on Google Cloud Run with `--min-instances 0`. Do not introduce persistent background workers, scheduled jobs, or always-on connections that would incur idle charges.

## 🔄 Development Workflow
1.  Fork the repository and branch from `main`.
2.  Install dependencies:
    ```bash
    python3 -m venv venv && source venv/bin/activate
    pip install -r requirements.txt
    python backend/db_init.py
    cd web && npm install
    ```
3.  Run locally:
    ```bash
    # Terminal 1: Backend
    uvicorn backend.main:app --host 0.0.0.0 --port 8000
    # Terminal 2: Frontend
    cd web && npm run dev
    ```
4.  Write test cases for any new agent logic or schema changes.
5.  Submit a Pull Request and ensure all tests pass.

## 📝 Commit Standards
We use Conventional Commits. Examples:
*   `feat(schema): add Depots and Shipments tables`
*   `fix(agent): handle multi-line SQL generation from Gemini`
*   `docs(walkthrough): update deployment screenshots`
