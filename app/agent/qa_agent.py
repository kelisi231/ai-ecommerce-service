from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from app.api.model.rag import RAGResponse, RAGSource
from app.service.retrieval import RetrievalService

SYSTEM_PROMPT = (
    "你是电商平台的智能客服助手，负责解答用户关于商品、政策、FAQ 等知识库问题。\n"
    "请严格遵守以下要求：\n"
    "1. 只能依据给定的参考资料回答，禁止编造资料中不存在的信息；\n"
    "2. 如果资料中没有相关信息，请如实回答“资料中没有找到相关信息”，并建议用户联系人工客服；\n"
    "3. 回答使用简体中文，简洁、口语化、友好，不需要提及资料的来源。"
)


class QAAgent:
    def __init__(self, retrieval_service: RetrievalService, llm):
        self.retrieval_service = retrieval_service
        self.llm = llm

    async def run(
            self,
            question: str,
            history: list[BaseMessage] | None = None,
    ) -> RAGResponse:
        chunks = await self.retrieval_service.retrieve(question)
        context = self._build_context(chunks)
        messages: list[BaseMessage] = [SystemMessage(content=SYSTEM_PROMPT)]
        if history:
            messages.extend(history)
        messages.append(
            HumanMessage(
                content=f"以下是参考资料：\n\n{context}\n\n用户问题：{question}"
            )
        )
        resp = await self.llm.ainvoke(messages)
        answer = resp.content if isinstance(resp.content, str) else str(resp.content)

        sources = [
            RAGSource(
                chunk_id=chunk.chunk_id,
                source=chunk.source,
                index=chunk.index,
                question=chunk.question,
                content=chunk.content,
                score=round(chunk.score, 4),
            )
            for chunk in chunks
        ]
        return RAGResponse(answer=answer, sources=sources)

    @staticmethod
    def _build_context(chunks):
        parts = []

        for i, chunk in enumerate(chunks, 1):
            parts.append(f"[{i}] 来源：{chunk.source} #{chunk.index}\n{chunk.content}")

        return "\n\n".join(parts)
