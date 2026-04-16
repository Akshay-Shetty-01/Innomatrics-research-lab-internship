from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from prompts.match_prompt import match_prompt

llm = ChatGroq(model="llama-3.1-8b-instant")
match_chain = match_prompt| llm.with_config({"run_name": "match"})| StrOutputParser()
