from langchain_core.documents import Document
from app.core.chunk.base_chunker import BaseChunker, build_metadata


class LineChunker(BaseChunker):
    def chunk(self, text: str, *, doc_id: str, source: str) -> list[Document]:
        # if line.strip() 判断是否为空
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return [Document(
            page_content=line,
            metadata=build_metadata(doc_id, source, i))
            for i, line in enumerate(lines)
        ]
