write("tools/ats_scorer.py", """
    # tools/ats_scorer.py
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
""")
