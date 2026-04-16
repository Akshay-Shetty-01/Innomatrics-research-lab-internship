from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from prompts.score_prompt import score_prompt

llm = ChatGroq(model="llama-3.1-8b-instant")
score_chain = score_prompt | llm.with_config({"run_name": "score"}) | StrOutputParser()
