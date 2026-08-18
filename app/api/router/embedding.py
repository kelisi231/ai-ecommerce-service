from fastapi import APIRouter
import app.api.lifespan.embedding_lifespan as embedding_lifespan
from app.api.model.embedding import EmbeddingResponse, EmbeddingRequest
from app.conf.embedding import DEVICE

router = APIRouter(prefix="/embedding", tags=["embedding"])

@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/info")
def info():
    return {"model": "bge-small-zh-v1.5", "dimension": 512, "device": DEVICE}


@router.post("/embed", response_model=EmbeddingResponse)
def embed(req: EmbeddingRequest):
    embeddings = embedding_lifespan.model.encode(
        req.inputs,
        normalize_embeddings=True,
        convert_to_numpy=True,
    ).tolist()
    return EmbeddingResponse(embeddings=embeddings)
