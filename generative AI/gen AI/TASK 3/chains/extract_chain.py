from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from prompts.extract_prompt import extract_prompt

llm = ChatGroq(model="llama-3.1-8b-instant")

extract_chain = extract_prompt | llm.with_config({"run_name": "extract"}) | StrOutputParser()