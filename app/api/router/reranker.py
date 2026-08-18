from fastapi import APIRouter

import app.api.lifespan.reranker_lifespan as reranker_lifespan
from app.api.model.reranker import RerankResponse, RerankRequest, RerankResult
from app.conf.reranker import DEVICE

router = APIRouter(prefix="/reranker", tags=["reranker"])


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/info")
def info():
    return {"model": "bge-reranker-base", "device": DEVICE}


@router.post("/rerank", response_model=RerankResponse)
def rerank(req: RerankRequest):
    docs = req.documents if req.documents is not None else req.texts
    scores = reranker_lifespan.model.predict(
        [[req.query, doc] for doc in docs],
        convert_to_numpy=True,
    ).tolist()

    ranked = sorted(range(len(docs)), key=lambda i: scores[i], reverse=True)
    results = [RerankResult(index=i, score=scores[i]) for i in ranked]
    if req.top_n is not None:
        results = results[: req.top_n]

    return RerankResponse(results=results)
