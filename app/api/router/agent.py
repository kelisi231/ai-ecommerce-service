from fastapi import APIRouter, Depends

from app.agent.supervisor_agent import SupervisorAgent
from app.api.dependencies import get_supervisor
from app.api.model.agent import AgentRequest, AgentResponse


router = APIRouter(
    prefix="/agent",
    tags=["agent"],
)

@router.post("/chat", response_model=AgentResponse)
async def chat(
        req: AgentRequest,
        supervisor: SupervisorAgent = Depends(get_supervisor),
):
    return await supervisor.run(
        session_id = req.session_id,
        user_id=req.user_id,
        question=req.question,
    )