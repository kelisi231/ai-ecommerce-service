from qdrant_client import AsyncQdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue

from app.conf.app_config import QdrantConfig


class QdrantRepository:
    def __init__(self, client: AsyncQdrantClient, qdrant_config: QdrantConfig):
        self.client = client
        self.qdrant_config = qdrant_config

    async def ensure_collection(self):
        if not await self.client.collection_exists(self.qdrant_config.collection_name):
            await self.client.create_collection(
                collection_name=self.qdrant_config.collection_name,
                vectors_config=VectorParams(
                    size=self.qdrant_config.embedding_size,
                    distance=Distance.COSINE,
                )
            )

    async def upsert_chunks(self, points: list[PointStruct]):
        await self.ensure_collection()
        await self.client.upsert(
            collection_name=self.qdrant_config.collection_name,
            points=points,
            wait=True,
        )

    async def delete_doc(self, doc_id: str):
        await self.ensure_collection()
        await self.client.delete(
            collection_name=self.qdrant_config.collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="doc_idx",
                        match=MatchValue(value=doc_id)
                    )
                ]
            ),
            wait=True
        )

    async def search(self, query_vector: list[float], top_k: int, score_threshold: float = 0.3):
        await self.ensure_collection()
        resp = await self.client.query_points(
            collection_name=self.qdrant_config.collection_name,
            query=query_vector,
            limit=top_k,
            score_threshold=score_threshold,
            with_payload=True,
        )

        return [
            {
                "chunk_id": p.payload["chunk_id"],
                "doc_idx": p.payload["doc_idx"],
                "source": p.payload["source"],
                "index": p.payload["index"],
                "question": p.payload.get("question"),
                "content": p.payload["content"],
                "score": p.score
            } for p in resp.points
        ]