import re
from langchain_core.documents import Document

from app.core.chunk.base_chunker import BaseChunker, build_metadata

ARTICLE_SPLIT = re.compile(r"^第.+[条章]", re.MULTILINE)


class ArticleChunker(BaseChunker):
    def chunk(self, text: str, *, doc_id: str, source: str) -> list[Document]:
        documents = []
        index = 0

        matches = list(ARTICLE_SPLIT.finditer(text))
        for i, match in enumerate(matches):
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            segment = text[match.start():end]

            documents.append(Document(page_content=segment, metadata=build_metadata(doc_id, source, index)))
            index += 1

        return documents
