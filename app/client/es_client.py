import asyncio
from elasticsearch import AsyncElasticsearch
from app.conf.app_config import app_config, ESConfig


class ESClient:
    def __init__(self, es_config: ESConfig):
        self.es_config = es_config
        self.client: AsyncElasticsearch | None = None

    def _get_url(self):
        return self.es_config.hosts

    def init(self):
        self.client = AsyncElasticsearch(hosts=self._get_url())

    async def close(self):
        await self.client.close()


es_client = ESClient(app_config.es)


if __name__ == "__main__":

    async def main():
        es_client.init()
        es_service = es_client.client

        if es_service and await es_service.ping():
            print("✅ AsyncElasticsearch 连接成功！\n")
            text_to_test = "人工智能客服系统"

            # 1. 测试 ik_smart (粗粒度切分)
            res_smart = await es_service.indices.analyze(
                body={"analyzer": "ik_smart", "text": text_to_test}
            )
            tokens_smart = [item["token"] for item in res_smart["tokens"]]
            print(f"👉 ik_smart 分词结果: {tokens_smart}")

            # 2. 测试 ik_max_word (细粒度切分)
            res_max = await es_service.indices.analyze(
                body={"analyzer": "ik_max_word", "text": text_to_test}
            )
            tokens_max = [item["token"] for item in res_max["tokens"]]
            print(f"👉 ik_max_word 分词结果: {tokens_max}")

        else:
            print("❌ ES 连接失败，请检查服务。")

        await es_client.close()

    asyncio.run(main())