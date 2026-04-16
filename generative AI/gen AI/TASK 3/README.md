# AI Resume Screening System with Tracing

## Project Overview
This project is an AI-powered Resume Screening System built using LangChain and Groq LLM.

It evaluates resumes based on a given job description and provides:
- Skill extraction
- Matching analysis
- Score (0–100)
- Explanation

---

## Features
- Resume vs Job Description comparison
- Skill extraction using LLM
- Match percentage calculation
- Score generation
- Explainable AI output
- LangSmith tracing for debugging

---

## Tech Stack
- Python
- LangChain
- LangSmith
- Groq (LLM)
- Jupyter Notebook in VScode

---

## Project Structure
project/
│── prompts/
│── chains/
│── data/
│── main.ipynb
│── requirements.txt


---

## Pipeline Flow
Resume → Extract → Match → Score → Explain


---

## Test Cases

| Candidate Type | Score |
|---------------|------|
| Strong        | High |
| Average       | Medium |
| Weak          | Low |

---

## LangSmith Tracing

### Pipeline View
(Add your pipeline screenshot here)
NSc1.png
---

### 🔹 Extract Step
(Add extract screenshot)
Nsc2.png
---

### Match Step
(Add match screenshot)
Nsc3.png
---

### Score Step
(Add score screenshot)
Nsc4.png
---

### Explain Step
(Add explain screenshot)
Nsc5.png
---

### Debug Case
(Add weak candidate screenshot)
Nsc6.png
---

## Environment Variables

Create `.env` file:

LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
GROQ_API_KEY=your_groq_api_key



---

## How to Run

```bash
pip install -r requirements.txt

Run notebook:
main.ipynb
