import asyncio
from uuid import uuid4

from langchain_core.documents import Document
from qdrant_client.models import PointStruct

from app.api.model.knowledge import DeleteResult, IngestResult, KnowledgeDoc
from app.core.chunk.extract_text import extract_text_by_type
from app.core.chunk.service import chunk_text
from app.repository.embedding_repository import EmbeddingRepository
from app.repository.es_repository import ESRepository
from app.repository.qdrant_repository import QdrantRepository


class KnowledgeIngestionService:
    def __init__(
            self,
            es_repository: ESRepository,
            qdrant_repository: QdrantRepository,
            embedding_repository: EmbeddingRepository
    ):
        self.es_repository = es_repository
        self.qdrant_repository = qdrant_repository
        self.embedding_repository = embedding_repository

    async def ingest(self, filename: str, content: bytes, doc_id: str | None = None) -> IngestResult:
        doc_id = doc_id or uuid4().hex
        text_type = await asyncio.to_thread(extract_text_by_type, filename, content)
        documents: list[Document] = await asyncio.to_thread(chunk_text, text_type, doc_id=doc_id, source=filename)
        if not documents:
            return IngestResult(
                doc_id=doc_id,
                file_name=filename,
                chunk_count=0
            )

        texts: list[str] = [doc.page_content for doc in documents]
        embeddings = await self.embedding_repository.embed(texts)

        points = []
        es_docs = []
        for doc, vector in zip(documents, embeddings):
            payload = dict(doc.metadata)
            payload["content"] = doc.page_content
            points.append(
                PointStruct(id=payload["chunk_id"], vector=vector, payload=payload)
            )
            es_docs.append(payload)

        await self.qdrant_repository.delete_doc(doc_id)
        await self.es_repository.delete_doc(doc_id)

        await self.qdrant_repository.upsert_chunks(points)
        await self.es_repository.bulk_index(es_docs)

        return IngestResult(
            doc_id=doc_id,
            file_name=filename,
            chunk_count=len(documents),
        )

    async def delete(self, doc_id: str):
        await self.qdrant_repository.delete_doc(doc_id)
        await self.es_repository.delete_doc(doc_id)

        return DeleteResult(doc_id=doc_id)

    async def list_docs(self) -> list[KnowledgeDoc]:
        docs = await self.es_repository.list_docs()
        return [KnowledgeDoc(**doc) for doc in docs]
