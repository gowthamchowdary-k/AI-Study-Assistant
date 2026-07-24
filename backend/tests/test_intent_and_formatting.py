import unittest

from intent.intent_router import IntentRouter
from formatter.response_formatter import ResponseFormatter


class LearningPlatformFoundationTests(unittest.TestCase):
    def test_intent_router_maps_actions(self):
        router = IntentRouter()

        self.assertEqual(router.classify("Generate quiz questions"), "generate_mcqs")
        self.assertEqual(router.classify("Summarize this chapter"), "summary")
        self.assertEqual(router.classify("Explain the concept simply"), "explain")

    def test_response_formatter_builds_structured_payload(self):
        formatter = ResponseFormatter()

        payload = formatter.format(
            title="Chapter Summary",
            answer="This section explains the core idea.",
            sources=["sample.pdf"],
            confidence=0.91,
            pages=[1, 2],
            follow_up_questions=["What is the main takeaway?"],
            study_tips=["Review key definitions"],
        )

        self.assertEqual(payload["title"], "Chapter Summary")
        self.assertEqual(payload["summary"], "This section explains the core idea.")
        self.assertEqual(payload["sources"][0], "sample.pdf")
        self.assertEqual(payload["confidence"], 0.91)
        self.assertEqual(payload["pages"], [1, 2])


if __name__ == "__main__":
    unittest.main()
