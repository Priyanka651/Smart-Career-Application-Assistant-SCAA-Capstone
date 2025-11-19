# 9) pipeline/run_pipeline.py
write("pipeline/run_pipeline.py", """
    # pipeline/run_pipeline.py
    from agents.jd_analyzer import analyze_jd
    from agents.resume_tailor import tailor_resume
    from agents.interview_prep import interview_prep
    from memory.memory_store import MemoryStore
    import json, time

    mem = MemoryStore("memory/memory_store.json")

    def run_end_to_end(jd_text_or_url: str, resume_pdf_path: str, user_id: str = "user1"):
        trace = {"trace_id": str(int(time.time()*1000)), "events": []}
        trace["events"].append({"step":"jd_fetch_and_analyze", "ts": time.time()})
        jd_analysis = analyze_jd(jd_text_or_url)
        mem.add_jd_signature(jd_analysis["jd_signature"], jd_analysis)
        trace["events"].append({"jd_analysis": {"skills_count": len(jd_analysis.get('skills', [])), "sig": jd_analysis.get('jd_signature')}})

        trace["events"].append({"step":"resume_tailoring", "ts": time.time()})
        tail = tailor_resume(resume_pdf_path, jd_analysis, user_id=user_id)
        trace["events"].append({"tailoring_result": {"ats_before": tail["ats_score_before"], "ats_after": tail["ats_score_after"]}})

        trace["events"].append({"step":"interview_prep", "ts": time.time()})
        ip = interview_prep(jd_analysis, tail["tailored_resume_text"])
        trace["events"].append({"interview": {"q_count": len(ip["questions"])}})

        result = {
            "trace": trace,
            "jd_analysis": jd_analysis,
            "tailoring": tail,
            "interview_prep": ip
        }
        return result
""")
print("All files created under", root)
