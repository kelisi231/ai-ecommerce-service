from  fastapi import  APIRouter, Depends
from app.agent.qa_agent import QAAgent
from app.api.dependencies import get_qa_agent
from app.api.model.rag import RAGQuery, RAGResponse


router = APIRouter(prefix="/rag", tags=["rag"])




@router.get("/health")
def health():
    return {"health": "ok"}

@router.post("/ask", response_model=RAGResponse)
async def  ask(req: RAGQuery, agent: QAAgent = Depends(get_qa_agent)):
    return await agent.run(req.question)