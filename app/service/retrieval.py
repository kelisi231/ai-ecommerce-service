from dataclasses import dataclass
from app.client.reranker_client import RerankerClient
from app.repository.embedding_repository import EmbeddingRepository
from app.repository.qdrant_repository import QdrantRepository
from app.repository.es_repository import ESRepository

RRF_K = 60


@dataclass
class ScoredChunk:
    chunk_id: str
    doc_idx: str
    source: str
    index: int
    question: str | None
    content: str
    score: float


class RetrievalService:
    def __init__(
            self,
            reranker_client: RerankerClient,
            embedding_repository: EmbeddingRepository,
            qdrant_repository: QdrantRepository,
            es_repository: ESRepository,

    ):
        self.reranker_client = reranker_client
        self.qdrant_repository = qdrant_repository
        self.es_repository = es_repository
        self.embedding_repository = embedding_repository

    @staticmethod
    # rrf融合
    def _rrf_fuse(hit_lists: list[list[dict]]) -> dict[str, ScoredChunk]:
        fused: dict[str, ScoredChunk] = {}
        for hits in hit_lists:
            for rank, hit in enumerate(hits, start=1):
                chunk_id = hit["chunk_id"]
                chunk = fused.get(chunk_id)
                if chunk is None:
                    chunk = ScoredChunk(
                        chunk_id=chunk_id,
                        doc_idx=hit["doc_idx"],
                        source=hit["source"],
                        index=hit["index"],
                        question=hit["question"],
                        content=hit["content"],
                        score=0.0
                    )
                    fused[chunk_id] = chunk
                chunk.score += 1.0 / (RRF_K + rank)
        return fused

    async def retrieve(
            self,
            question: str,
            *,
            qdrant_top_k: int = 20,
            es_top_k: int = 10,
            rerank_candidates: int = 20,
            final_top_k: int = 5,
    ) -> list[ScoredChunk]:

        query_vector = await self.embedding_repository.embed_question(question)
        qdrant_hits = await self.qdrant_repository.search(query_vector, qdrant_top_k)
        es_hits = await self.es_repository.search(question, es_top_k)

        fused = self._rrf_fuse([qdrant_hits, es_hits])
        rrf_candidates: list[ScoredChunk] = sorted(fused.values(), key=lambda x: x.score, reverse=True)
        candidates: list[ScoredChunk] = rrf_candidates[:rerank_candidates]
        if not candidates:
            return []

        texts = [c.content for c in candidates]

        resp = await self.reranker_client.client.post(
            "/reranker/rerank",
            json={"query": question, "texts": texts, "top_n": final_top_k},
        )

        resp.raise_for_status()

        ranked = []
        # {"result": [{"index":"1", "score": "0.9"}, {}, {}, {}, {}]}
        for item in resp.json()["results"]:
            # 根据重拍后的索引对candidate进行重排
            chunk = candidates[item["index"]]
            chunk.score = item["score"]
            ranked.append(chunk)
        return ranked
