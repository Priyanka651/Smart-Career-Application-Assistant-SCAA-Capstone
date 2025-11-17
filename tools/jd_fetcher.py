# tools/jd_fetcher.py
"""
Simple job description fetcher.
- If `text_or_url` looks like a URL, attempt to fetch and extract main text (basic).
- Otherwise, return the input as-is (assume it's JD text).
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def is_url(s: str) -> bool:
    try:
        o = urlparse(s)
        return bool(o.scheme and o.netloc)
    except:
        return False

def fetch_jd(text_or_url: str, timeout=8) -> str:
    if not text_or_url:
        return ""
    if not is_url(text_or_url):
        return text_or_url
    try:
        resp = requests.get(text_or_url, timeout=timeout, headers={"User-Agent": "scaa-bot/1.0"})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        # Basic extraction: join all paragraph text
        paragraphs = soup.find_all(['p', 'li', 'h1','h2','h3'])
        text = "\n\n".join([p.get_text(separator=" ", strip=True) for p in paragraphs])
        return text.strip() or soup.get_text(separator="\n")
    except Exception as e:
        return f"[ERROR_FETCHING_URL] {e}"

# Example usage
if __name__ == "__main__":
    example = "https://example.com/job"
    print(fetch_jd("Senior Frontend Engineer React TypeScript experience required"))

