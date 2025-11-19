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
