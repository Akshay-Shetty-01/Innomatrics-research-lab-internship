from langchain_core.prompts import PromptTemplate

score_prompt = PromptTemplate(
    input_variables=["match_data"],
    template="""
You are a scoring system.

Use match_percentage to assign score.

Rules:
- >= 70 → 90–100
- 40–69 → 50–79
- < 40 → 0–49

IMPORTANT:
- Return ONLY JSON
- Do NOT explain
- Do NOT add any text

Format:
{{ "score": number }}

Match Data:
{match_data}
"""
)