from pydantic import Field, BaseModel


class RerankRequest(BaseModel):
    query: str = Field(..., description="查询文本")
    texts: list[str] = Field(default_factory=list, description="候选文本列表")
    documents: list[str] | None = Field(None, description="候选文本别名（与 texts 二选一）")
    top_n: int | None = Field(None, description="返回前 N 条，默认全部")


class RerankResult(BaseModel):
    index: int
    score: float


class RerankResponse(BaseModel):
    results: list[RerankResult]
