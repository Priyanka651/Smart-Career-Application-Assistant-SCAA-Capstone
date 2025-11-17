# pipeline/run_pipeline.py
"""
Simple orchestrator (A2A-like) for running the three agents in sequence.
This acts as the "coordinator" when testing in Kaggle.
"""
from agents.jd_analyzer import analyze_jd
from agents.resume_tailor import tailor_resume
from agents.interview_prep import interview_prep
from memory.memory_store import MemoryStore
import json, time

mem = MemoryStore("memory/memory_store.json")

def run_end_to_end(jd_text_or_url: str, resume_pdf_path: str, user_id: str = "user1"):
    trace = {"trace_id": str(int(time.time()*1000)), "events": []}
    # 1) JD Analyzer
    trace["events"].append({"step":"jd_fetch_and_analyze", "ts": time.time()})
    jd_analysis = analyze_jd(jd_text_or_url)
    mem.add_jd_signature(jd_analysis["jd_signature"], jd_analysis)
    trace["events"].append({"jd_analysis": jd_analysis})

    # 2) Resume Tailor (pause/approve simulated by direct call)
    trace["events"].append({"step":"resume_tailoring", "ts": time.time()})
    tail = tailor_resume(resume_pdf_path, jd_analysis, user_id=user_id)
    trace["events"].append({"tailoring_result": {"ats_before": tail["ats_score_before"], "ats_after": tail["ats_score_after"]}})

    # 3) Interview Prep
    trace["events"].append({"step":"interview_prep", "ts": time.time()})
    ip = interview_prep(jd_analysis, tail["tailored_resume_text"])
    trace["events"].append({"interview": {"q_count": len(ip["questions"])}})

    # Save trace & return structured result
    result = {
        "trace": trace,
        "jd_analysis": jd_analysis,
        "tailoring": tail,
        "interview_prep": ip
    }
    return result

# Example demo runner
if __name__ == "__main__":
    demo = run_end_to_end("We need a React + TypeScript engineer with AWS experience", "sample_resume.pdf", user_id="demo_user")
    print(json.dumps(demo, indent=2)[:2000])
