import unittest

from context_builder import ContextBuilder
from search import search_chunks, similarity_from_distance


class RAGPipelineTests(unittest.TestCase):
    def test_similarity_scaling(self):
        self.assertEqual(similarity_from_distance(0.0), 1.0)
        self.assertEqual(similarity_from_distance(10.0), 0.0)

    def test_context_builder_deduplicates_and_orders(self):
        builder = ContextBuilder(max_chunks=2)
        results = [
            {"text": "alpha", "file": "doc.pdf", "page": 1, "chunk_id": "a"},
            {"text": "alpha", "file": "doc.pdf", "page": 1, "chunk_id": "a"},
            {"text": "beta", "file": "doc.pdf", "page": 2, "chunk_id": "b"},
        ]

        context, sources, pages, chunk_ids = builder.build(results)

        self.assertIn("alpha", context)
        self.assertIn("beta", context)
        self.assertEqual(sources, ["doc.pdf"])
        self.assertEqual(pages, [1, 2])
        self.assertEqual(chunk_ids, ["a", "b"])


if __name__ == '__main__':
    unittest.main()
