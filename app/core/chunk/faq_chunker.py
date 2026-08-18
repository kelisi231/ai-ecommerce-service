import re
from langchain_core.documents import Document
from app.core.chunk.base_chunker import BaseChunker, build_metadata


# 获取每一个 “问题：”
QA_SPLIT = re.compile(r"^问题：", re.MULTILINE)
MAX_QAT = 800


class FAQChunker(BaseChunker):
    def chunk(self, text: str, *, doc_id: str, source: str) -> list[Document]:
        documents = []
        index = 0

        # 获取每一个 “ 问题：” 的索引值 并组合成列表
        matches = list(QA_SPLIT.finditer(text))

        # 遍历出每一个 “ 问题：” 的索引值
        for i, match in enumerate(matches):
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            segment = text[match.start():end].strip()
            question = segment.splitlines()[0]

            documents.append(
                Document(
                    page_content=segment,
                    metadata=build_metadata(doc_id, source, index, question=question)
                )
            )
            index += 1

        return documents
