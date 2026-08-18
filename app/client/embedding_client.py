import httpx

from app.conf.app_config import EmbeddingConfig, app_config


class EmbeddingClient:
    def __init__(self, embedding_config: EmbeddingConfig):
        self.embedding_config = embedding_config
        self.client: httpx.AsyncClient | None = None

    def init(self):
        self.client = httpx.AsyncClient(base_url=self.embedding_config.url, timeout=60)

    async def close(self):
        if self.client:
            await self.client.aclose()


embedding_client = EmbeddingClient(app_config.embedding)


if __name__ == "__main__":
    import asyncio

    async def main():
        embedding_client.init()
        try:
            health = await embedding_client.client.get("/embedding/health")
            health.raise_for_status()
            print("✅ Embedding 服务连接成功！", health.json())

            resp = await embedding_client.client.post(
                "/embedding/embed",
                json={"inputs": ["如何办理退款", "退换货政策说明"]},
            )
            resp.raise_for_status()
            embeddings = resp.json()["embeddings"]
            print(f"📁 向量数量: {len(embeddings)}, 维度: {len(embeddings[0])}")
            print(f"👉 第一个向量前3位: {embeddings[0][:3]}")
        except httpx.HTTPError as e:
            print(f"❌ 测试失败: {e}")
        finally:
            await embedding_client.close()

    asyncio.run(main())
