from httpx import AsyncClient

EMBEDDING_BATCH_SIZE = 30


class EmbeddingRepository:
    def __init__(self, client: AsyncClient):
        self.client = client

    async def embed(self, texts: list[str]) -> list[list[float]]:
        embeddings: list[list[float]] = []

        for i in range(0, len(texts), EMBEDDING_BATCH_SIZE):
            batch = texts[i: i + EMBEDDING_BATCH_SIZE]
            resp = await self.client.post("/embedding/embed", json={"inputs": batch})
            resp.raise_for_status()
            embeddings.extend(resp.json()["embeddings"])

        if len(embeddings) != len(texts):
            raise ValueError(f"向量数量不匹配: 期望 {len(texts)}, 实际 {len(embeddings)}")

        return embeddings

    async def embed_question(self, text: str) -> list[float]:
        return (await self.embed([text]))[0]