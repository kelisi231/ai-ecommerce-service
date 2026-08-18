from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import agent, knowledge, login, rag
from app.client.embedding_client import embedding_client
from app.client.es_client import es_client
from app.client.mysql_client import mysql_client
from app.client.qdrant_client_manager import qdrant_manager
from app.client.reranker_client import reranker_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    mysql_client.init()
    qdrant_manager.init()
    es_client.init()
    embedding_client.init()
    reranker_client.init()

    yield

    await mysql_client.close()
    await es_client.close()
    await qdrant_manager.close()
    await embedding_client.close()
    await reranker_client.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router)
app.include_router(knowledge.router)
app.include_router(rag.router)
app.include_router(agent.router)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
