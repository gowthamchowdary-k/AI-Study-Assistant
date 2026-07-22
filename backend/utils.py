"""
Common utility functions used throughout the backend.
"""

import re
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
# PDF Validation
# -------------------------------------------------------

def allowed_file(filename: str) -> bool:
    return (
        filename.lower().endswith(".pdf")
    )


def clean_filename(filename: str) -> str:
    return secure_filename(filename)