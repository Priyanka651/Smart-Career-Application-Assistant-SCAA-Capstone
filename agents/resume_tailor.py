# agents/resume_tailor.py

write("agents/resume_tailor.py", """
    # agents/resume_tailor.py
    from tools.resume_parser import parse_pdf
    from tools.ats_scorer import simple_keyword_score
    from tools.skill_matcher import extract_skills_from_text
    import uuid, time

    def generate_tailored_bullets(resume_text: str, jd_keywords: list):
        sents = [s.strip() for s in resume_text.split("\\n") if s.strip()]
        matched = []
        for s in sents:
            for k in jd_keywords:
                if k.lower() in s.lower() and s not in matched:
                    matched.append(s)
        if not matched:
            matched = [f"Experienced with {', '.join(jd_keywords[:4])}."]
        return matched[:12]

    def tailor_resume(pdf_path: str, jd_analysis: dict, user_id: str = "default_user"):
        t0 = time.time()
        resume_text = parse_pdf(pdf_path)
        keywords = jd_analysis.get("keywords", []) if jd_analysis else extract_skills_from_text(resume_text)
        before_score = simple_keyword_score(resume_text, keywords)
        tailored_bullets = generate_tailored_bullets(resume_text, keywords)
        tail_text = "\\n".join(tailored_bullets)
        after_score = simple_keyword_score(tail_text + resume_text, keywords)
        result = {
            "status": "ok",
            "tailored_bullets": tailored_bullets,
            "ats_score_before": before_score,
            "ats_score_after": after_score,
            "tailored_resume_text": tail_text,
            "artifact_id": str(uuid.uuid4()),
            "meta": {"took_seconds": time.time()-t0}
        }
        return result
""")
