from pydantic import BaseModel, Field

from app.api.model.rag import RAGSource


class AgentRequest(BaseModel):
    session_id: str = Field(..., min_length=1, description="会话 ID")
    question: str = Field(..., min_length=1, description="用户问题")
    user_id: int | None = Field(None, description="用户 ID，查询订单时必填")


class AgentResponse(BaseModel):
    agent: str
    answer: str
    sources: list[RAGSource] | None = None