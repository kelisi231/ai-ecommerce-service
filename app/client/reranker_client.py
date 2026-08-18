import httpx

from app.conf.app_config import RerankerConfig, app_config


class RerankerClient:
    def __init__(self, reranker_config: RerankerConfig):
        self.reranker_config = reranker_config
        self.client: httpx.AsyncClient | None = None

    def init(self):
        self.client = httpx.AsyncClient(base_url=self.reranker_config.url, timeout=60)

    async def close(self):
        if self.client:
            await self.client.aclose()


reranker_client = RerankerClient(app_config.reranker)


if __name__ == "__main__":
    import asyncio

    async def main():
        reranker_client.init()
        try:
            health = await reranker_client.client.get("/reranker/health")
            health.raise_for_status()
            print("✅ Reranker 服务连接成功！", health.json())

            resp = await reranker_client.client.post(
                "/reranker/rerank",
                json={
                    "query": "怎么申请退款",
                    "texts": [
                        "我们支持7天无理由退换货",
                        "今天天气很好",
                        "订单可以在后台申请退款",
                    ],
                },
            )
            resp.raise_for_status()
            results = resp.json()["results"]
            print(f"📁 重排结果(降序): {[(x['index'], round(x['score'], 4)) for x in results]}")
        except httpx.HTTPError as e:
            print(f"❌ 测试失败: {e}")
        finally:
            await reranker_client.close()

    asyncio.run(main())
