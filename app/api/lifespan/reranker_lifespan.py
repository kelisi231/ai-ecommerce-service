from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.conf.reranker import MODEL_PATH, DEVICE, MAX_SEQ_LENGTH
from sentence_transformers import CrossEncoder
from app.api.router import reranker

model: CrossEncoder | None = None


@asynccontextmanager
async def lifespan(_: FastAPI):
    global model
    model = CrossEncoder(MODEL_PATH, device=DEVICE, max_length=MAX_SEQ_LENGTH)
    yield
    del model


app = FastAPI(title="Reranker Service", lifespan=lifespan)
app.include_router(reranker.router)
