# tools/ats_scorer.py
"""
Simple ATS scorer: counts overlap between JD keywords and resume text.
Returns a float in [0.0, 1.0]
"""
import re
from typing import List

def simple_keyword_score(resume_text: str, keywords: List[str]) -> float:
    if not keywords:
        return 0.0
    text = (resume_text or "").lower()
    matches = 0
    for k in keywords:
        if k and k.lower() in text:
            matches += 1
    return matches / len(keywords)

# Example usage
if __name__ == "__main__":
    resume = "I used React and TypeScript with AWS and Docker"
    keywords = ["react","typescript","aws","kubernetes"]
    print(simple_keyword_score(resume, keywords))
