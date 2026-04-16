from langchain_core.prompts import PromptTemplate

match_prompt = PromptTemplate(
    input_variables=["resume_data", "job_description"],
    template="""
You are an AI recruiter.

Compare resume data with job description.

Steps:
1. Extract required skills from the job description.
2. Extract candidate skills from resume data.
3. Count how many required skills are present in the resume.
4. Calculate match percentage.

Formula:
match_percentage = (matched_skills / total_required_skills) * 100

Rules:
- Do NOT assume skills
- Count only exact matches (case-insensitive)
- Ignore tools in percentage calculation
- match_percentage MUST be an integer (0–100), NOT a string
- Do NOT include % symbol

IMPORTANT:
- Be accurate in counting
- Do not hallucinate missing or extra skills
- Use only given data

Return ONLY valid JSON:

{{  
  "matching_skills": [],  
  "missing_skills": [],  
  "match_percentage": 0  
}}

Resume Data:
{resume_data}

Job Description:
{job_description}
"""
)