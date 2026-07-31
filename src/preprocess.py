from __future__ import annotations

import re


# ---------------------------------------------------------------------------
# Compiled regex patterns (compiled once at import time for efficiency)
# ---------------------------------------------------------------------------

_URL_PATTERN       = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
_HTML_TAG_PATTERN  = re.compile(r"<[^>]+>")
_EMAIL_PATTERN     = re.compile(r"\b[\w.+-]+@[\w-]+\.[a-z]{2,}\b", re.IGNORECASE)
_PHONE_PATTERN     = re.compile(
    r"(\+?\d{1,3}[\s.-]?)?(\(?\d{2,4}\)?[\s.-]?)?\d{3,5}[\s.-]?\d{4,6}"
)
_SPECIAL_CHAR_PATTERN = re.compile(r"[^a-z0-9\s]")   # applied after lowercasing
_WHITESPACE_PATTERN   = re.compile(r"\s+")


# ---------------------------------------------------------------------------
# clean_text()
# ---------------------------------------------------------------------------

def clean_text(text: str) -> str:
    """
    Clean and normalise raw resume or job-description text for NLP use.

    Pipeline (in order):
        1. Lowercase the entire string.
        2. Remove URLs  (``http://…``, ``https://…``, ``www.…``).
        3. Strip HTML tags (``<tag>…</tag>``).
        4. Remove e-mail addresses.
        5. Remove phone numbers (international and local formats).
        6. Remove punctuation and non-alphanumeric special characters
           (only ``[a-z0-9 ]`` are kept after this step).
        7. Collapse multiple spaces / newlines into a single space.
        8. Strip leading / trailing whitespace.

    Args:
        text (str): Raw input text from a resume or job description.

    Returns:
        str: Cleaned, normalised string ready for embedding or skill extraction.
             Returns an empty string if ``text`` is None or empty.

    Example:
        >>> clean_text("Visit https://google.com. Email: hr@co.io  Ph: +91-9876543210")
        'visit email ph'
    """
    if not text:
        return ""

    # 1. Lowercase
    text = text.lower()

    # 2. Remove URLs
    text = _URL_PATTERN.sub(" ", text)

    # 3. Remove HTML tags
    text = _HTML_TAG_PATTERN.sub(" ", text)

    # 4. Remove e-mail addresses  (before phone, to avoid partial digit matches)
    text = _EMAIL_PATTERN.sub(" ", text)

    # 5. Remove phone numbers
    text = _PHONE_PATTERN.sub(" ", text)

    # 6. Remove punctuation / special characters (keep letters, digits, spaces)
    text = _SPECIAL_CHAR_PATTERN.sub(" ", text)

    # 7 & 8. Collapse whitespace and strip
    text = _WHITESPACE_PATTERN.sub(" ", text).strip()

    return text
