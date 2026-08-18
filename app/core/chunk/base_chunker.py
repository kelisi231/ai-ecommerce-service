from abc import ABC, abstractmethod
from uuid import uuid4

from langchain_core.documents import Document


def build_metadata(doc_id: str, source: str, index: int, question: str | None = None) -> dict:
    meta = {
        "chunk_id": str(uuid4()),
        "doc_idx": doc_id,
        "source": source,
        "index": index,

    }
    if question:
        meta["question"] = question
    return meta


class BaseChunker(ABC):
    # 抽象类 继承它的都要有chunk函数 必须返回list[Document]
    @abstractmethod
    # *号 左边位置传参和关键字传参， 右边强制关键字传参
    def chunk(self, text: str, *, doc_id: str, source: str) -> list[Document]:
        pass
