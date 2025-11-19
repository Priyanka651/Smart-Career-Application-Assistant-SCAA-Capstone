%%writefile pipeline/run_pipeline.py
from agents.jd_analyzer import analyze_jd
from agents.resume_tailor import tailor_resume
from agents.interview_prep import interview_prep

def run_end_to_end(jd_text: str, resume_text: str):
    step1 = analyze_jd(jd_text)
    step2 = tailor_resume(jd_text, resume_text)
    step3 = interview_prep(step1, step2.get("tailored_resume", ""))
    
    return {
        "JD_Analysis": step1,
        "Tailored_Resume": step2,
        "Interview_Prep": step3
    }
