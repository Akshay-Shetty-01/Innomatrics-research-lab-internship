from langchain_core.prompts import PromptTemplate

extract_prompt = PromptTemplate(
    input_variables=["resume"],
    template="""
You are an AI Resume Parser.

Extract the following:
- Skills
- Tools
- Experience (in years)

Rules:
- Do NOT assume anything
- Convert experience into a number (e.g., "3 years" → 3)

Resume:
{resume}

Return output in JSON format:
{{
  "skills": [],
  "tools": [],
  "experience": 0
}}
"""
)