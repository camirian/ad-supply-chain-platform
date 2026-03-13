import streamlit as st
import sqlite3
import pandas as pd
import sys
import os

# Add the project root to sys.path so we can import from rag
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rag.nlp_agent import query_agent

st.set_page_config(
    page_title="A&D Supply Chain Agent",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a premium feel
st.markdown("""
<style>
    .chat-container {
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .user-msg {
        background-color: #f0f2f6;
    }
    .agent-msg {
        background-color: #e6f3ff;
        border-left: 4px solid #0066cc;
    }
    .stApp {
        background-color: #ffffff;
    }
    h1 {
        color: #1a1a1a;
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

st.title("✈️ A&D Supply Chain Intelligence Agent")
st.markdown("""
Welcome to the Supply Chain AI Agent. This system maps natural language to a relational SQL database 
containing Parts, Suppliers, and Work Orders. Ask questions about your inventory, lead times, or supplier performance!
""")

# --- Sidebar ---
with st.sidebar:
    st.header("🏢 Database Overview")
    st.markdown("This agent has access to the following relational schema:")
    
    st.subheader("Tables")
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'supply_chain.db')
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        tables = ['Suppliers', 'Parts', 'WorkOrders']
        for table in tables:
            with st.expander(f"📦 {table}"):
                df = pd.read_sql_query(f"SELECT * FROM {table} LIMIT 5", conn)
                st.dataframe(df, use_container_width=True)
                st.caption(f"Showing sample from {table}")
        
    except Exception as e:
        st.error(f"Database connection error: {e}")

    st.divider()
    
    st.subheader("💡 Example Queries")
    examples = [
        "Which supplier has the best rating?",
        "Show me all blocked work orders.",
        "What is the total value of stock we hold for Inconel Fasteners?",
        "List all parts supplied by AeroTech Dynamics."
    ]
    for ex in examples:
        st.info(f"\"{ex}\"")

# --- Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your supply chain tracking agent. How can I assist you today?"}
    ]

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle user input
if prompt := st.chat_input("Ask about parts, suppliers, or work orders..."):
    # Append user prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing database..."):
            
            # Warn if API key is dummy
            if os.environ.get("OPENAI_API_KEY") == "sk-placeholder-for-testing" or not os.environ.get("OPENAI_API_KEY"):
                st.warning("⚠️ OpenAI API Key is not set! Using dummy agent response mode.")
                response = f"[Simulated Response]: I see you asked about '{prompt}'. To fully resolve this against the SQLite database, please set a valid OPENAI_API_KEY."
            else:
                response = query_agent(prompt)
                
            st.markdown(response)
            
    # Append assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
