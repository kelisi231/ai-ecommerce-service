import asyncio
from qdrant_client import AsyncQdrantClient
from app.conf.app_config import app_config, QdrantConfig


class QdrantClient:
    def __init__(self, qdrant_config: QdrantConfig):
        self.qdrant_config = qdrant_config
        self.client: AsyncQdrantClient | None = None

    def _get_url(self):
        return f"http://{self.qdrant_config.host}:{self.qdrant_config.port}"

    def init(self):
        self.client = AsyncQdrantClient(self._get_url())

    async def close(self):
        await self.client.close()


qdrant_manager = QdrantClient(app_config.qdrant)



if __name__ == '__main__':

    async def main():
        client = AsyncQdrantClient(host="localhost", port=6333)
        try:
            collections = await client.get_collections()
            print("✅ Qdrant 连接成功！")
            print(f"📁 当前已有集合: {[c.name for c in collections.collections]}")
        except Exception as e:
            print(f"❌ 连接失败: {e}")
        finally:
            await client.close()


    asyncio.run(main())