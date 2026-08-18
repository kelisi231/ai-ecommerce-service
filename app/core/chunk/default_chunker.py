from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.core.chunk.base_chunker import BaseChunker, build_metadata


class DefaultChunker(BaseChunker):
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", "。", "！", "？", "；", "，", "、", " ", ""]
        )

    def chunk(self, text: str, *, doc_id: str, source: str) -> list[Document]:
        return [Document(page_content=piece, metadata=build_metadata(doc_id, source, i)) for i, piece in
                enumerate(self._splitter.split_text(text))]
