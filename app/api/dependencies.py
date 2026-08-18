from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.general_agent import GeneralAgent
from app.agent.llm import llm
from app.agent.order_agent import OrderAgent
from app.agent.qa_agent import QAAgent
from app.client.es_client import es_client
from app.client.mysql_client import mysql_client
from app.client.qdrant_client_manager import qdrant_manager
from app.client.embedding_client import embedding_client
from app.client.reranker_client import reranker_client
from app.conf.app_config import app_config
from app.repository.embedding_repository import EmbeddingRepository
from app.repository.login import UserLoginRepository
from app.repository.order import OrderRepository
from app.repository.qdrant_repository import QdrantRepository
from app.repository.es_repository import ESRepository
from app.service.login import UserLoginService
from app.service.knowledge import KnowledgeIngestionService
from app.service.order import OrderService
from app.service.retrieval import RetrievalService
from app.agent.supervisor_agent import SupervisorAgent


async def get_db_session():
    async with mysql_client.session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def user_login_service(session: AsyncSession = Depends(get_db_session)):
    login_repository = UserLoginRepository(session)
    return UserLoginService(login_repository)


async def get_knowledge_service():
    es_repo = ESRepository(es_client.client, app_config.es)
    qdrant_repo = QdrantRepository(qdrant_manager.client, app_config.qdrant)
    embedding_repo = EmbeddingRepository(embedding_client.client)

    return KnowledgeIngestionService(es_repo, qdrant_repo, embedding_repo)



async def get_qa_agent():
    es_repo = ESRepository(es_client.client, app_config.es)
    qdrant_repo = QdrantRepository(qdrant_manager.client, app_config.qdrant)
    embedding_repo = EmbeddingRepository(embedding_client.client)
    retriever_service = RetrievalService(reranker_client, embedding_repo, qdrant_repo, es_repo)

    return QAAgent(retriever_service, llm)


async def get_order_agent(session: AsyncSession = Depends(get_db_session)):
    order_repo = OrderRepository(session)
    oder_service = OrderService(order_repo)
    return OrderAgent(oder_service, llm)


async def get_general_agent():
    return GeneralAgent(llm)


async def get_supervisor(
    qa_agent: QAAgent = Depends(get_qa_agent),
    order_agent: OrderAgent = Depends(get_order_agent),
    general_agent: GeneralAgent = Depends(get_general_agent),
):
    return SupervisorAgent(
        llm,
        qa_agent,
        order_agent,
        general_agent,
    )