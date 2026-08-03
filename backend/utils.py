"""
Common utility functions used throughout the backend.
"""

import re
import os
from werkzeug.utils import secure_filename


# -------------------------------------------------------
# Follow-up Question Detection
# -------------------------------------------------------

FOLLOW_UP_WORDS = {
    "it",
    "this",
    "that",
    "these",
    "those",
    "they",
    "them",
    "more",
    "again",
    "continue",
    "explain",
    "elaborate",
    "describe",
    "details",
    "detail",
    "simple",
    "simplify",
    "example",
    "examples",
    "why",
    "how"
}


def is_follow_up(question: str) -> bool:
    """
    Returns True if the question looks like a follow-up.

    Example:
        Explain more.
        Give an example.
        Why?
        Continue.
    """

    words = set(
        re.findall(r"\b\w+\b", question.lower())
    )

    return len(words.intersection(FOLLOW_UP_WORDS)) > 0


# -------------------------------------------------------
# Greeting Detection
# -------------------------------------------------------

GREETINGS = {
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening"
}


def is_greeting(question: str) -> bool:
    return question.lower().strip() in GREETINGS


# -------------------------------------------------------
# File Validation
# -------------------------------------------------------

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".pptx", ".txt", ".png", ".jpg", ".jpeg", ".webp"}

def allowed_file(filename: str) -> bool:
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def clean_filename(filename: str) -> str:
    import os
    return secure_filename(filename)