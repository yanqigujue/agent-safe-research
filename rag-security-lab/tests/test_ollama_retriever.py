from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from rag_security_lab.components.retrievers import OllamaEmbeddingRetriever
from rag_security_lab.models import Document, Query


class _FakeResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return self.payload


class _FakeSession:
    instances: list["_FakeSession"] = []

    def __init__(self) -> None:
        self.post_calls = 0
        self.__class__.instances.append(self)

    def get(self, url: str, timeout: int) -> _FakeResponse:
        return _FakeResponse(
            {
                "models": [
                    {
                        "name": "test-embedding:latest",
                        "digest": "test-digest",
                        "details": {"embedding_length": 2},
                        "capabilities": ["embedding"],
                    }
                ]
            }
        )

    def post(self, url: str, json: dict, timeout: int) -> _FakeResponse:
        self.post_calls += 1
        vectors = {
            "alpha": [1.0, 0.0],
            "beta": [0.0, 1.0],
        }
        return _FakeResponse({"embeddings": [vectors[text] for text in json["input"]]})


class OllamaEmbeddingRetrieverTest(unittest.TestCase):
    def test_ranking_and_cache_reuse(self) -> None:
        with tempfile.TemporaryDirectory() as temp_value:
            _FakeSession.instances.clear()
            with patch("rag_security_lab.components.retrievers.requests.Session", _FakeSession):
                retriever = OllamaEmbeddingRetriever(
                    {
                        "model": "test-embedding",
                        "project_root": temp_value,
                        "cache_path": "embedding-cache.sqlite3",
                        "batch_size": 16,
                    }
                )
                documents = [
                    Document(doc_id="doc-alpha", text="alpha"),
                    Document(doc_id="doc-beta", text="beta"),
                ]
                queries = [Query(query_id="query-alpha", text="alpha")]

                first = retriever.retrieve(documents, queries, top_k=2)
                second = retriever.retrieve(documents, queries, top_k=2)

            self.assertEqual(first[0][0].document.doc_id, "doc-alpha")
            self.assertEqual(second[0][0].document.doc_id, "doc-alpha")
            self.assertEqual(_FakeSession.instances[0].post_calls, 1)
            self.assertEqual(retriever.stats["cache_misses"], 2)
            self.assertEqual(retriever.stats["cache_hits"], 4)
            self.assertEqual(retriever.stats["embedding_dimension"], 2)
            self.assertTrue((Path(temp_value) / "embedding-cache.sqlite3").exists())


if __name__ == "__main__":
    unittest.main()
