from langchain_core.documents import Document

from app.core.chunk.article_chunker import ArticleChunker
from app.core.chunk.default_chunker import DefaultChunker
from app.core.chunk.faq_chunker import FAQChunker
from app.core.chunk.line_chunker import LineChunker
from app.core.chunk.judgment import is_faq, is_article, is_line_based

faq_chunker = FAQChunker()
article_chunker = ArticleChunker()
line_chunker = LineChunker()
default_chunker = DefaultChunker()


def chunk_text(text: str, *, doc_id: str, source: str) -> list[Document]:
    if is_faq(text):
        return faq_chunker.chunk(text, doc_id=doc_id, source=source)

    if is_article(text):
        return article_chunker.chunk(text, doc_id=doc_id, source=source)

    if is_line_based(text):
        return line_chunker.chunk(text, doc_id=doc_id, source=source)

    return default_chunker.chunk(text, doc_id=doc_id, source=source)
