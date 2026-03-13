# System Architecture: A&D Supply Chain AI Agent

This document outlines the formal C4 (Context, Container, Component) architecture for the **A&D Supply Chain Platform**, pivoted to a decoupled FastAPI and React stack designed for zero-billing serverless execution on Google Cloud Run.

This formalization substantiates Applied AI Architect and Systems Engineering software design claims (`CPS_CAP_05`, `CPS_NAV_01`).

## 1. System Context Diagram
*The high-level view showing how users and external systems interact with the platform.*

```mermaid
flowchart TD
    classDef person fill:#08427b,color:#fff,stroke:#052e56,stroke-width:2px
    classDef system fill:#1168bd,color:#fff,stroke:#0b4884,stroke-width:2px
    classDef ext_system fill:#999999,color:#fff,stroke:#6b6b6b,stroke-width:2px

    Manager(["Supply Chain Manager<br>[Person]"]):::person
    
    Agent["A&D Supply Chain Agent<br>[System]"]:::system
    GeminiAPI["Google Gemini API<br>[External System]"]:::ext_system

    Manager -->|"Queries inventory, suppliers, <br>and lead times"| Agent
    Agent -->|"Prompts text-to-SQL logic block"| GeminiAPI
```

## 2. Container Diagram
*The distinct deployable units that make up the software system.*

```mermaid
flowchart TD
    classDef person fill:#08427b,color:#fff,stroke:#052e56,stroke-width:2px
    classDef container fill:#438dd5,color:#fff,stroke:#3c7fc0,stroke-width:2px
    classDef ext_system fill:#999999,color:#fff,stroke:#6b6b6b,stroke-width:2px
    classDef db fill:#438dd5,color:#fff,stroke:#3c7fc0,stroke-width:2px
    classDef edgeLabel fill:none,stroke:none

    Manager(["Supply Chain Manager<br>[Person]"]):::person
    GeminiAPI["Google Gemini API<br>[External System]"]:::ext_system

    subgraph CloudRun ["Google Cloud Run Environment (Zero Billing)"]
        Frontend["React Web Frontend<br>[Vite, SPA]<br><br>Provides chat UI and<br>schema visualizer"]:::container
        Backend["FastAPI Backend<br>[Python 3.10+]<br><br>Handles LLM orchestration<br>and SQL execution"]:::container
        Database[("SQLite Database<br>[Ephemeral File]<br><br>Stores dummy supply chain<br>snapshots")]:::db
    end

    Manager -->|"Uses UI chat"| Frontend
    Frontend -->|"RESTful API Calls (JSON)"| Backend
    Backend -->|"Reads/Executes schemas"| Database
    Backend -->|"Sends context & questions<br>for query rendering"| GeminiAPI
    
    style CloudRun fill:none,stroke:#666,stroke-width:2px,stroke-dasharray: 5 5
```

## 3. Component Diagram (Backend & Submodules)
*Zooming into the Python FastAPI Backend container to view internal logic blocks.*

```mermaid
flowchart TD
    classDef component fill:#85bbf0,color:#000,stroke:#5b82a7,stroke-width:2px
    classDef ext_system fill:#999999,color:#fff,stroke:#6b6b6b,stroke-width:2px
    classDef db fill:#438dd5,color:#fff,stroke:#3c7fc0,stroke-width:2px
    classDef edgeLabel fill:none,stroke:none

    GeminiAPI["Google Gemini API<br>[External System]"]:::ext_system
    Database[("SQLite DB<br>[Local File]")]:::db

    subgraph BackendApp ["FastAPI Application"]
        Router["main.py<br>[FastAPI Endpoints]<br><br>Routes /api/chat & /api/schema"]:::component
        AgentModule["nlp_agent.py<br>[LangChain Pipeline]<br><br>Interacts with DB & Gemini"]:::component
        SQLTool["QuerySQLDatabaseTool<br>[LangChain Utility]<br><br>Executes safe SELECTs"]:::component
    end

    Router -->|"Passes parameters"| AgentModule
    AgentModule -->|"Validates queries"| SQLTool
    SQLTool --> Database
    AgentModule -->|"Sends schema DB schema & prompts"| GeminiAPI
    
    style BackendApp fill:none,stroke:#666,stroke-width:2px,stroke-dasharray: 5 5
```

## Architectural Design Decisions & Trade-offs
1. **Monolithic Storage (SQLite):** For MVP velocity and Cloud Run cost-controls (Scale to Zero), SQLite provides a simple, self-contained persistence layer perfectly demonstrating relational logic (`CPS_NAV_01`) without paying for Cloud SQL per-hour connectivity. 
2. **Decoupled Architecture**: By pivoting away from Streamlit to a FastAPI + React structure, the frontend UI and the backend logic can scale totally independently or be migrated to different serverless handlers (e.g. AWS Lambda / Cloudfront).
3. **Google Gemini Context Allocation**: Gemini `1.5-Flash` serves as an industry-leading zero-cost NLP pipeline. The `langchain-google-genai` integration isolates the complexity of context window tracking.
