# A&D Supply Chain AI Agent

A full-stack Minimum Viable Product (MVP) demonstrating an Aerospace & Defense supply chain conversational agent. 
This project leverages a LangChain text-to-SQL architecture to query a local relational database using natural language, presented through a responsive and modern Streamlit frontend.

> **Traceability**: This repository specifically fulfills the following Enterprise IT and Applied AI capabilities from my portfolio:
> *   **CPS_CAP_05**: A&D Supply Chain AI Agent (Full-stack MVP utilizing Streamlit and LLM RAG pipelines)
> *   **CPS_NAV_01**: Architected the Shop Workload Management System for depot production control, leveraging relational database systems

## Features
- **Relational Backend**: A `SQLite` database modeling typical A&D supply chain entities (Parts, Suppliers, Work Orders).
- **Conversational RAG / NLP Agent**: Natural language to SQL translation using `LangChain` and OpenAI models.
- **Premium Frontend**: An accessible and aesthetic Streamlit web app providing users with a chat interface, database schema exploration, and suggested queries.

## Getting Started

### Prerequisites
- Python 3.10+
- OpenAI API Key

### Installation

1. **Clone the repository and install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Initialize the database:**
```bash
python backend/db_init.py
```
This script creates `data/supply_chain.db` and seeds it with mock data including titanium compressor blades, actuators, and various defense-grade suppliers.

3. **Set your API Key:**
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

4. **Run the Application:**
```bash
streamlit run frontend/app.py
```
This will open the conversational UI in your browser at `http://localhost:8501/`.

## Architecture Details
For a deeper technical dive into the schema design, prompt orchestration, and text-to-SQL flow, please see [ARCHITECTURE.md](docs/ARCHITECTURE.md).
