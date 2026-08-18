from pydantic import  BaseModel, Field

class EmbeddingRequest(BaseModel):
    inputs: list[str] = Field(..., min_length=1, description="待编码文本列表 ")


class EmbeddingResponse(BaseModel):
    embeddings: list[list[float]]
