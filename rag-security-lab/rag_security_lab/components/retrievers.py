from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from contextlib import closing
from pathlib import Path
from typing import Any

import numpy as np
import requests
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

from ..models import Document, Query, RetrievalHit
from ..registry import RETRIEVERS


def _to_hits(scores: np.ndarray, docs: list[Document], top_k: int) -> list[list[RetrievalHit]]:
    results: list[list[RetrievalHit]] = []
    for row in scores:
        order = row.argsort()[::-1][:top_k]
        results.append(
            [RetrievalHit(rank, float(row[index]), docs[int(index)]) for rank, index in enumerate(order, start=1)]
        )
    return results


def _row_minmax(matrix: np.ndarray) -> np.ndarray:
    mins = matrix.min(axis=1, keepdims=True)
    maxs = matrix.max(axis=1, keepdims=True)
    denominator = maxs - mins
    denominator[denominator == 0] = 1
    return (matrix - mins) / denominator


class _TfidfBase:
    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    def _matrices(self, docs: list[Document], queries: list[Query]):
        vectorizer = TfidfVectorizer(
            analyzer=self.config.get("analyzer", "char_wb"),
            ngram_range=tuple(self.config.get("ngram_range", [2, 5])),
            min_df=int(self.config.get("min_df", 1)),
            sublinear_tf=bool(self.config.get("sublinear_tf", True)),
        )
        doc_matrix = vectorizer.fit_transform([doc.text for doc in docs])
        query_matrix = vectorizer.transform([query.text for query in queries])
        return doc_matrix, query_matrix


@RETRIEVERS.register("tfidf")
class TfidfRetriever(_TfidfBase):
    def retrieve(self, docs: list[Document], queries: list[Query], top_k: int) -> list[list[RetrievalHit]]:
        doc_matrix, query_matrix = self._matrices(docs, queries)
        return _to_hits(cosine_similarity(query_matrix, doc_matrix), docs, top_k)


@RETRIEVERS.register("lsa")
class LsaRetriever(_TfidfBase):
    def retrieve(self, docs: list[Document], queries: list[Query], top_k: int) -> list[list[RetrievalHit]]:
        doc_matrix, query_matrix = self._matrices(docs, queries)
        maximum = min(doc_matrix.shape[0] - 1, doc_matrix.shape[1] - 1)
        components = min(int(self.config.get("components", 64)), maximum)
        if components < 1:
            return _to_hits(cosine_similarity(query_matrix, doc_matrix), docs, top_k)
        svd = TruncatedSVD(n_components=components, random_state=int(self.config.get("seed", 2026)))
        doc_dense = normalize(svd.fit_transform(doc_matrix))
        query_dense = normalize(svd.transform(query_matrix))
        return _to_hits(query_dense @ doc_dense.T, docs, top_k)


@RETRIEVERS.register("hybrid_lsa")
class HybridLsaRetriever(_TfidfBase):
    def retrieve(self, docs: list[Document], queries: list[Query], top_k: int) -> list[list[RetrievalHit]]:
        doc_matrix, query_matrix = self._matrices(docs, queries)
        sparse = cosine_similarity(query_matrix, doc_matrix)
        maximum = min(doc_matrix.shape[0] - 1, doc_matrix.shape[1] - 1)
        components = min(int(self.config.get("components", 64)), maximum)
        if components < 1:
            return _to_hits(sparse, docs, top_k)
        svd = TruncatedSVD(n_components=components, random_state=int(self.config.get("seed", 2026)))
        doc_dense = normalize(svd.fit_transform(doc_matrix))
        query_dense = normalize(svd.transform(query_matrix))
        dense = query_dense @ doc_dense.T
        alpha = min(max(float(self.config.get("alpha", 0.5)), 0.0), 1.0)
        combined = alpha * _row_minmax(sparse) + (1 - alpha) * _row_minmax(dense)
        return _to_hits(combined, docs, top_k)


@RETRIEVERS.register("ollama_embedding")
class OllamaEmbeddingRetriever:
    """Dense cosine retrieval backed by Ollama's batch embedding API.

    Embeddings are cached in SQLite by model digest and exact content hash. A
    changed poison passage is recomputed while unchanged clean documents are
    reused across experiments.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.base_url = str(config.get("base_url", "http://localhost:11434")).rstrip("/")
        self.model = str(config.get("model", "bge-m3-ms-q4"))
        self.batch_size = max(1, int(config.get("batch_size", 32)))
        self.timeout = int(config.get("timeout", 300))
        self.max_retries = max(1, int(config.get("max_retries", 3)))
        project_root = Path(config.get("project_root", "."))
        cache_value = Path(config.get("cache_path", ".cache/rag_security_lab/embeddings.sqlite3"))
        self.cache_path = cache_value if cache_value.is_absolute() else project_root / cache_value
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.model_info = self._load_model_info()
        self.model_key = f"{self.model}@{self.model_info.get('digest') or 'unknown'}"
        self.stats = {
            "model": self.model,
            "model_digest": self.model_info.get("digest"),
            "embedding_dimension": None,
            "cache_path": str(self.cache_path.resolve()),
            "cache_hits": 0,
            "cache_misses": 0,
            "api_batches": 0,
            "embedded_text_count": 0,
        }
        self._initialize_cache()

    def _load_model_info(self) -> dict[str, Any]:
        response = self.session.get(self.base_url + "/api/tags", timeout=min(self.timeout, 30))
        response.raise_for_status()
        candidates = response.json().get("models", [])
        requested_base = self.model.split(":", 1)[0]
        for item in candidates:
            candidate_name = str(item.get("name") or item.get("model") or "")
            if candidate_name == self.model or candidate_name.split(":", 1)[0] == requested_base:
                return {
                    "name": candidate_name,
                    "digest": item.get("digest"),
                    "size": item.get("size"),
                    "details": item.get("details", {}),
                    "capabilities": item.get("capabilities", []),
                }
        raise ValueError(f"Ollama model is not installed: {self.model}")

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.cache_path)
        connection.execute("PRAGMA journal_mode=WAL")
        return connection

    def _initialize_cache(self) -> None:
        with closing(self._connect()) as connection, connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS embeddings (
                    model_key TEXT NOT NULL,
                    text_hash TEXT NOT NULL,
                    dimension INTEGER NOT NULL,
                    vector BLOB NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (model_key, text_hash)
                )
                """
            )

    @staticmethod
    def _text_hash(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _read_cached(self, hashes: list[str]) -> dict[str, np.ndarray]:
        if not hashes:
            return {}
        found: dict[str, np.ndarray] = {}
        with closing(self._connect()) as connection, connection:
            for start in range(0, len(hashes), 500):
                chunk = hashes[start : start + 500]
                placeholders = ",".join("?" for _ in chunk)
                rows = connection.execute(
                    f"SELECT text_hash, dimension, vector FROM embeddings "
                    f"WHERE model_key = ? AND text_hash IN ({placeholders})",
                    [self.model_key, *chunk],
                )
                for text_hash, dimension, blob in rows:
                    vector = np.frombuffer(blob, dtype=np.float32)
                    if vector.size == int(dimension):
                        found[str(text_hash)] = vector.copy()
        return found

    def _write_cached(self, values: dict[str, np.ndarray]) -> None:
        if not values:
            return
        with closing(self._connect()) as connection, connection:
            connection.executemany(
                "INSERT OR REPLACE INTO embeddings(model_key, text_hash, dimension, vector) VALUES (?, ?, ?, ?)",
                [
                    (self.model_key, text_hash, int(vector.size), vector.astype(np.float32).tobytes())
                    for text_hash, vector in values.items()
                ],
            )

    def _request_batch(self, texts: list[str]) -> list[np.ndarray]:
        last_error: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.session.post(
                    self.base_url + "/api/embed",
                    json={"model": self.model, "input": texts, "truncate": True},
                    timeout=self.timeout,
                )
                response.raise_for_status()
                embeddings = response.json().get("embeddings", [])
                if len(embeddings) != len(texts):
                    raise ValueError(
                        f"Ollama returned {len(embeddings)} embeddings for {len(texts)} inputs"
                    )
                self.stats["api_batches"] += 1
                self.stats["embedded_text_count"] += len(texts)
                return [np.asarray(vector, dtype=np.float32) for vector in embeddings]
            except (requests.RequestException, ValueError) as exc:
                last_error = exc
                if attempt < self.max_retries:
                    time.sleep(min(2**attempt, 10))
        raise RuntimeError(f"Ollama embedding request failed after {self.max_retries} attempts: {last_error}")

    def _embed(self, texts: list[str]) -> np.ndarray:
        hashes = [self._text_hash(text) for text in texts]
        unique_text_by_hash = dict(zip(hashes, texts))
        cached = self._read_cached(list(unique_text_by_hash))
        missing_hashes = [text_hash for text_hash in unique_text_by_hash if text_hash not in cached]
        self.stats["cache_hits"] += len(unique_text_by_hash) - len(missing_hashes)
        self.stats["cache_misses"] += len(missing_hashes)

        generated: dict[str, np.ndarray] = {}
        for start in range(0, len(missing_hashes), self.batch_size):
            batch_hashes = missing_hashes[start : start + self.batch_size]
            batch_texts = [unique_text_by_hash[text_hash] for text_hash in batch_hashes]
            batch_vectors = self._request_batch(batch_texts)
            generated.update(zip(batch_hashes, batch_vectors))
        self._write_cached(generated)
        cached.update(generated)

        vectors = np.stack([cached[text_hash] for text_hash in hashes]).astype(np.float32)
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1
        vectors /= norms
        self.stats["embedding_dimension"] = int(vectors.shape[1])
        return vectors

    def retrieve(self, docs: list[Document], queries: list[Query], top_k: int) -> list[list[RetrievalHit]]:
        if not docs or not queries:
            return [[] for _ in queries]
        doc_vectors = self._embed([doc.text for doc in docs])
        query_vectors = self._embed([query.text for query in queries])
        return _to_hits(query_vectors @ doc_vectors.T, docs, top_k)

    def get_run_info(self) -> dict[str, Any]:
        return {
            "type": "ollama_embedding",
            "base_url": self.base_url,
            "model_info": self.model_info,
            "cache": dict(self.stats),
        }
