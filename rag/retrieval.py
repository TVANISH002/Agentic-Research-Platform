from __future__ import annotations

import numpy as np
from sentence_transformers import SentenceTransformer
from core.config import settings
from core.state import ChunkRecord


class SemanticRetriever:
    def __init__(self) -> None:
        self.model = SentenceTransformer(settings.embedding_model)
        self.chunk_embeddings: np.ndarray | None = None
        self.chunks: list[ChunkRecord] = []

    def index(self, chunks: list[ChunkRecord]) -> None:
        self.chunks = chunks
        texts = [c.text for c in chunks]
        if not texts:
            self.chunk_embeddings = np.empty((0, 384))
            return
        embeddings = self.model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        self.chunk_embeddings = np.array(embeddings)

    def retrieve(self, queries: list[str], top_k: int | None = None) -> list[ChunkRecord]:
        if self.chunk_embeddings is None or not len(self.chunks):
            return []
        top_k = top_k or settings.top_k_chunks
        query_embeddings = self.model.encode(queries, normalize_embeddings=True, show_progress_bar=False)
        score_map: dict[int, float] = {}
        for q_emb in query_embeddings:
            scores = self.chunk_embeddings @ q_emb
            best_idx = np.argsort(scores)[::-1][:top_k]
            for idx in best_idx:
                score_map[idx] = max(score_map.get(idx, -1.0), float(scores[idx]))
        ranked = sorted(score_map.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [self.chunks[idx] for idx, _ in ranked]
