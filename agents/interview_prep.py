# agents/interview_prep.py
"""
Interview Prep agent skeleton.
- Accepts JD analysis + tailored resume text and returns likely questions + sample answers
- Uses simple heuristics; later replace with Gemini LLM prompt for richer answers
"""
from tools.skill_matcher import extract_skills_from_text
import time

def generate_questions(jd_analysis: dict, tailored_resume_text: str, top_n=8):
    skills = jd_analysis.get("skills", []) if jd_analysis else extract_skills_from_text(tailored_resume_text)
    questions = []
    # basic patterns
    for s in skills[:top_n]:
        questions.append(f"Can you explain your experience with {s}?")
    questions += [
        "Tell me about a time you faced a technical challenge and how you solved it.",
        "Why are you interested in this role and company?"
    ]
    return questions[:top_n]

def generate_answers(questions: list, tailored_resume_text: str):
    # Placeholder: produce short structured answers referencing resume phrases
    answers = []
    for q in questions:
        # simplistic answer generation: pull sentences from resume that mention a keyword in q
        answers.append("Sample answer based on resume. (Replace with LLM-generated answer.)")
    return answers

def interview_prep(jd_analysis: dict, tailored_resume_text: str):
    t0 = time.time()
    qs = generate_questions(jd_analysis, tailored_resume_text)
    ans = generate_answers(qs, tailored_resume_text)
    return {"status":"ok", "questions": qs, "answers": ans, "meta":{"took_seconds": time.time()-t0}}

if __name__ == "__main__":
    print("interview_prep loaded")

