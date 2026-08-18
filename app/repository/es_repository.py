from elasticsearch.helpers import async_bulk

from app.conf.app_config import ESConfig


class ESRepository:
    def __init__(self, client, es_config: ESConfig):
        self.client = client
        self.es_config = es_config

    async def ensure_index(self):
        index_name = self.es_config.index_name
        if not await self.client.indices.exists(index=index_name):
            await self.client.indices.create(
                index=index_name,
                mappings={
                    "properties": {
                        "chunk_id": {"type": "keyword"},
                        "doc_idx": {"type": "keyword"},
                        "source": {"type": "keyword"},
                        "index": {"type": "integer"},
                        "question": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart"
                        },
                        "content": {
                            "type": "text",
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_smart"
                        },
                    }
                }
            )

    async def bulk_index(self, docs: list[dict]):
        await self.ensure_index()
        if not docs:
            return

        actions = [
            {
                "_op_type": "index",
                "_index": self.es_config.index_name,
                "_id": doc["chunk_id"],
                "_source": doc,
            }
            for doc in docs
        ]

        await async_bulk(self.client, actions, refresh=True)

    async def delete_doc(self, doc_id: str):
        await self.ensure_index()
        await self.client.delete_by_query(
            index=self.es_config.index_name,
            query={"term": {"doc_idx": doc_id}},
            refresh=True,
        )

    async def list_docs(self) -> list[dict]:
        await self.ensure_index()
        resp = await self.client.search(
            index=self.es_config.index_name,
            size=0,
            aggs={
                "docs": {
                    "terms": {
                        "field": "doc_idx",
                        "size": 1000,
                        "order": {"_key": "desc"},
                    },
                    "aggs": {
                        "source": {
                            "top_hits": {
                                "size": 1,
                                "_source": ["source"],
                            }
                        },
                        "chunk_count": {"value_count": {"field": "index"}},
                    },
                }
            },
        )

        buckets = resp["aggregations"]["docs"]["buckets"]
        return [
            {
                "doc_id": bucket["key"],
                "file_name": bucket["source"]["hits"]["hits"][0]["_source"]["source"],
                "chunk_count": bucket["chunk_count"]["value"],
            }
            for bucket in buckets
        ]

    async def search(self, query: str, top_k: int):
        await self.ensure_index()
        resp = await self.client.search(
            index=self.es_config.index_name,
            query={
                "bool": {
                    "should": [
                        {"match": {"content": {"query": query}}},
                        {"match": {"question": {"query": query, "boost": 3.0}}},
                    ],
                    "minimum_should_match": 1,
                }
            },
            size=top_k,
        )

        return [
            {
                "chunk_id": h["_source"]["chunk_id"],
                "doc_idx": h["_source"]["doc_idx"],
                "source": h["_source"]["source"],
                "index": h["_source"]["index"],
                "question": h["_source"].get("question"),
                "content": h["_source"]["content"],
                "score": h["_score"],
            }
            for h in resp["hits"]["hits"]
        ]
