import os
from rag.nlp_agent import get_sql_agent
from langchain.globals import set_debug
set_debug(True)

import logging
logging.basicConfig(level=logging.DEBUG)

question = "List all suppliers located in Seattle."
print(f"Testing Question: {question}")
chain = get_sql_agent(api_key=os.environ.get("GEMINI_API_KEY", ""))
try:
    response = chain.invoke({"question": question})
    print("Response:", response)
except Exception as e:
    print("Error:", e)
