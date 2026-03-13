import os
import sys
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import QuerySQLDatabaseTool
from langchain.prompts import PromptTemplate
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def get_sql_agent(db_uri="sqlite:///data/supply_chain.db"):
    """
    Initializes and returns a LangChain Runnable that translates a natural 
    language question into a SQL query, executes it against the local SQLite 
    database, and formulates a human-readable response using Gemini.
    """
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = "fake-key-for-testing"
        print("Warning: GOOGLE_API_KEY not set in environment.", file=sys.stderr)

    # Resolve absolute path for SQLite
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "supply_chain.db")
    db_uri_absolute = f"sqlite:///{db_path}"

    db = SQLDatabase.from_uri(db_uri_absolute)
    
    # Use Gemini via langchain_google_genai
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    
    execute_query = QuerySQLDatabaseTool(db=db)
    write_query = create_sql_query_chain(llm, db)
    
    answer_prompt = PromptTemplate.from_template(
        """Given the following user question, corresponding SQL query, and SQL result, answer the user question conversationally.
        
Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
    )
    
    answer = answer_prompt | llm | StrOutputParser()
    
    chain = (
        RunnablePassthrough.assign(query=write_query).assign(
            result=itemgetter("query") | execute_query
        )
        | answer
    )
    
    return chain

def query_agent(question: str) -> str:
    """
    Convenience function to invoke the SQL agent with a given question.
    """
    chain = get_sql_agent()
    try:
        response = chain.invoke({"question": question})
        return response
    except Exception as e:
        return f"Error executing query: {str(e)}"

if __name__ == "__main__":
    sample_question = "Which supplier has the highest rating, and what part do they supply?"
    print(f"Question: {sample_question}")
    print(f"Answer: {query_agent(sample_question)}")
