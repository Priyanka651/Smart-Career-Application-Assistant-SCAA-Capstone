# agents/jd_analyzer.py
"""
JD Analyzer agent skeleton.
- Uses tools/jd_fetcher.py and tools/skill_matcher.py
- Returns structured JSON analysis.
"""
import hashlib
import time
from tools.jd_fetcher import fetch_jd
from tools.skill_matcher import extract_skills_from_text

def make_signature(text: str) -> str:
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return h[:12]

def analyze_jd(text_or_url: str) -> dict:
    start = time.time()
    jd_text = fetch_jd(text_or_url)
    skills = extract_skills_from_text(jd_text)
    signature = make_signature(jd_text)
    analysis = {
        "status": "ok",
        "jd_text_snippet": jd_text[:800],
        "skills": skills,
        "keywords": skills,
        "red_flags": [],  # simple placeholder
        "jd_signature": signature,
        "meta": {"len_chars": len(jd_text), "took_seconds": time.time() - start}
    }
    return analysis

# Quick test when run directly
if __name__ == "__main__":
    print(analyze_jd("We need a React + TypeScript front-end engineer with AWS and Docker."))

