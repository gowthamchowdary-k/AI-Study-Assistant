import unittest
from unittest.mock import patch

from services.chat_service import process_chat


class ChatServiceContextTests(unittest.TestCase):
    @patch("services.chat_service.save_context")
    @patch("services.chat_service.ask_ai")
    @patch("services.chat_service.build_context")
    @patch("services.chat_service.search_chunks")
    @patch("services.chat_service.get_chunks")
    @patch("services.chat_service.get_index")
    @patch("services.chat_service.get_context")
    def test_process_chat_uses_retrieved_context_in_prompt(
        self,
        mock_get_context,
        mock_get_index,
        mock_get_chunks,
        mock_search_chunks,
        mock_build_context,
        mock_ask_ai,
        mock_save_context,
    ):
        mock_get_context.return_value = None
        mock_get_index.return_value = object()
        mock_get_chunks.return_value = [{"text": "doc chunk"}]
        mock_search_chunks.return_value = [
            {
                "distance": 0.5,
                "text": "document information",
                "file": "paper_3.pdf",
                "page": 1,
                "chunk_id": "paper_3::p1::c1",
            }
        ]
        mock_build_context.return_value = (
            "Document context that should reach the prompt.",
            ["paper_3.pdf"],
            [1],
        )
        mock_ask_ai.return_value = "Grounded answer"

        result = process_chat("Explain acne from the uploaded document", action_id="explain")

        self.assertIn("Document context that should reach the prompt.", result["prompt"])
        self.assertEqual(result["sources"], ["paper_3.pdf"])
        self.assertEqual(result["pages"], [1])


if __name__ == "__main__":
    unittest.main()
