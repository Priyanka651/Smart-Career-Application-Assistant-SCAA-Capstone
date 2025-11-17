# tools/skill_matcher.py
"""
Simple keyword/skill extraction and matching.
- `extract_skills_from_text` uses heuristic & basic regex to find capitalized tokens and common tech words.
- `get_keyword_list_from_jd` returns a normalized set of candidate keywords.
"""
import re

COMMON_SKILLS = [
    "python","java","javascript","react","angular","vue","typescript","sql","aws","gcp","azure",
    "docker","kubernetes","html","css","node","flask","django","tensorflow","pytorch","ml"
]

def normalize_token(tok: str) -> str:
    return re.sub(r'[^a-z0-9\+\#\-]', '', tok.lower())

def get_keyword_list_from_jd(jd_text: str):
    text = jd_text or ""
    tokens = re.findall(r"[A-Za-z\+\#\-]{2,}", text)
    tokens_norm = {normalize_token(t) for t in tokens}
    skills = sorted({s for s in tokens_norm if s in COMMON_SKILLS})
    # also return top N capitalized phrases heuristically
    caps = re.findall(r"\b([A-Z][a-zA-Z0-9\+\#\-]{1,})\b", text)
    caps_norm = [normalize_token(c) for c in caps][:20]
    return list(dict.fromkeys(skills + caps_norm))  # keep order, unique

def extract_skills_from_text(text: str, top_k=25):
    kws = get_keyword_list_from_jd(text)
    return kws[:top_k]

# Example usage
if __name__ == "__main__":
    jd = "We need a React + TypeScript developer experienced with AWS, Docker, and Kubernetes"
    print(extract_skills_from_text(jd))

