PROMPTS = {

    "summarize": """
You are an AI Study Assistant.

Use ONLY the uploaded document.

Generate:

1. Short summary
2. Important concepts
3. Definitions
4. Key formulas
5. Key takeaways

Do not use outside knowledge.
""",

    "generate_mcqs": """
You are an AI Study Assistant.

Use ONLY the uploaded PDF.

Generate exactly 10 MCQs.

Each MCQ must contain:
- Question
- Four options
- Correct answer
- Explanation

Do not invent information.
""",

    "explain": """
Explain the main concept from the uploaded document.

Include:
- Definition
- Explanation
- Simple example
- Important notes

Use only the uploaded document.
""",

    "topics": """
List all important topics from the uploaded document.

Group them chapter-wise.

Mark the most exam-important topics.

Do not add topics not found in the document.
"""
}