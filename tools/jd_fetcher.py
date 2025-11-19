write("tools/jd_fetcher.py", """
    # tools/jd_fetcher.py
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
            paragraphs = soup.find_all(['p', 'li', 'h1','h2','h3'])
            text = "\\n\\n".join([p.get_text(separator=" ", strip=True) for p in paragraphs])
            return text.strip() or soup.get_text(separator="\\n")
        except Exception as e:
            return f\"[ERROR_FETCHING_URL] {e}\"
""")

# 2) tools/resume_parser.py
write("tools/resume_parser.py", """
    # tools/resume_parser.py
    import os
    def parse_pdf_with_pdfplumber(path: str) -> str:
        try:
            import pdfplumber
        except ImportError:
            raise
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\\n"
        return text

    def parse_pdf(path: str) -> str:
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            raise FileNotFoundError(f\"Resume file not found: {path}\")
        try:
            return parse_pdf_with_pdfplumber(path)
        except Exception:
            try:
                from PyPDF2 import PdfReader
                reader = PdfReader(path)
                text = ""
                for p in reader.pages:
                    text += p.extract_text() or ""
                return text
            except Exception as e:
                raise RuntimeError(f\"All parsing methods failed: {e}\")
""")
