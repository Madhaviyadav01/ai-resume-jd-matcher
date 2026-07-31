from __future__ import annotations

import io
from typing import Union

import pdfplumber
from docx import Document


# ---------------------------------------------------------------------------
# 1. extract_text_from_pdf()
# ---------------------------------------------------------------------------

def extract_text_from_pdf(pdf_file: Union[str, bytes, io.IOBase]) -> str:
    """
    Extract plain text from a PDF file using pdfplumber.

    Args:
        pdf_file: A file path (str), raw bytes, or any file-like object
                  (e.g. from ``st.file_uploader`` or ``open("...", "rb")``).

    Returns:
        str: All extracted page text joined by newlines.
             Returns an empty string if extraction fails or the PDF has no text.
    """
    try:
        # pdfplumber.open() accepts both file paths and file-like objects.
        # If bytes are passed, wrap them in BytesIO first.
        if isinstance(pdf_file, (bytes, bytearray)):
            pdf_file = io.BytesIO(pdf_file)

        with pdfplumber.open(pdf_file) as pdf:
            pages_text = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages_text.append(text)
            return "\n".join(pages_text)

    except Exception as exc:
        print(f"[parser] PDF extraction error: {exc}")
        return ""


# ---------------------------------------------------------------------------
# 2. extract_text_from_docx()
# ---------------------------------------------------------------------------

def extract_text_from_docx(docx_file: Union[str, bytes, io.IOBase]) -> str:
    """
    Extract plain text from a DOCX file using python-docx.

    Args:
        docx_file: A file path (str), raw bytes, or any file-like object
                   (e.g. from ``st.file_uploader``).

    Returns:
        str: Paragraph text joined by newlines.
             Returns an empty string if extraction fails.
    """
    try:
        if isinstance(docx_file, (bytes, bytearray)):
            docx_file = io.BytesIO(docx_file)

        doc = Document(docx_file)
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n".join(paragraphs)

    except Exception as exc:
        print(f"[parser] DOCX extraction error: {exc}")
        return ""


# ---------------------------------------------------------------------------
# 3. extract_text()  — Dispatcher
# ---------------------------------------------------------------------------

def extract_text(file_obj) -> str:
    """
    Dispatcher that routes a file object to the correct extractor based on
    its file-name extension (``.pdf`` or ``.docx``).

    Supports:
      • Streamlit ``UploadedFile`` objects (have a ``.name`` attribute)
      • Plain file paths passed as strings
      • Raw bytes (fallback: tries PDF then DOCX)

    Args:
        file_obj: An ``UploadedFile``, file path string, or bytes.

    Returns:
        str: Extracted raw text, or an empty string on failure/unknown type.
    """
    # ── Determine extension ───────────────────────────────────────────────
    name: str = ""

    if hasattr(file_obj, "name"):          # Streamlit UploadedFile
        name = file_obj.name
    elif isinstance(file_obj, str):        # plain file path
        name = file_obj
    # bytes: no name available — fall through to extension == ""

    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""

    # ── Dispatch ──────────────────────────────────────────────────────────
    if ext == "pdf":
        # For Streamlit UploadedFile, read bytes and pass to extractor
        if hasattr(file_obj, "read"):
            return extract_text_from_pdf(file_obj.read())
        return extract_text_from_pdf(file_obj)

    elif ext == "docx":
        if hasattr(file_obj, "read"):
            return extract_text_from_docx(file_obj.read())
        return extract_text_from_docx(file_obj)

    else:
        # Unknown extension — try PDF first, then DOCX
        raw = file_obj.read() if hasattr(file_obj, "read") else file_obj
        result = extract_text_from_pdf(raw)
        if not result and isinstance(raw, (bytes, bytearray)):
            result = extract_text_from_docx(raw)
        return result
