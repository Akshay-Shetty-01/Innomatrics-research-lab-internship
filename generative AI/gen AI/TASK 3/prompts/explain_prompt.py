from langchain_core.prompts import PromptTemplate

explain_prompt = PromptTemplate(
    input_variables=["score", "match_data"],
    template="""
You are an AI system explaining a candidate evaluation.

IMPORTANT:
- The score is already calculated correctly
- You MUST explain based on the given score
- DO NOT contradict the score
- DO NOT recalculate anything

Rules:
- Use only given match_data
- Keep explanation consistent with score
- No assumptions

Format:
- Strengths:
- Missing Skills:
- Final Reason:

Score:
{score}

Match Data:
{match_data}
"""
)