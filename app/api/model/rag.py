from pydantic import BaseModel


class RAGQuery(BaseModel):
    question: str


class RAGSource(BaseModel):
    chunk_id: str
    source: str
    index: int
    question: str | None = None
    content: str
    score: float


class RAGResponse(BaseModel):
    answer: str
    sources: list[RAGSource]