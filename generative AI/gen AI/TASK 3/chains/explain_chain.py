from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from prompts.explain_prompt import explain_prompt

llm = ChatGroq(model="llama-3.1-8b-instant")
explain_chain = explain_prompt | llm.with_config({"run_name": "explain"}) | StrOutputParser()
