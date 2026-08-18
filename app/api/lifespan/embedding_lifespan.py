from contextlib import asynccontextmanager
from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
from sentence_transformers.sentence_transformer.modules import Normalize, Pooling, Transformer
from app.conf.embedding import MODEL_PATH, MAX_SEQ_LENGTH, DEVICE
from app.api.router import  embedding
model: SentenceTransformer | None = None


@asynccontextmanager
async def lifespan(_: FastAPI):
    global model
    transformer = Transformer(MODEL_PATH, max_seq_length=MAX_SEQ_LENGTH)
    pooling = Pooling(transformer.get_embedding_dimension(), pooling_mode="mean")
    model = SentenceTransformer(
        modules=[transformer, pooling, Normalize()],
        device=DEVICE,
    )
    yield
    del model


app = FastAPI(title="Embedding Service", lifespan=lifespan)
app.include_router(embedding.router)