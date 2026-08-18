from loguru import logger

from app.agent.general_agent import GeneralAgent
from app.agent.memory import conversation_memory
from app.agent.order_agent import OrderAgent
from app.agent.qa_agent import QAAgent
from app.agent.supervisor_graph import build_supervisor_graph
from app.api.model.agent import AgentResponse


class SupervisorAgent:
    def __init__(
            self,
            llm,
            qa_agent: QAAgent,
            order_agent: OrderAgent,
            general_agent: GeneralAgent,
    ):
        self.general_agent = general_agent
        self.graph = build_supervisor_graph(llm, qa_agent, order_agent, general_agent)


    async def run(
        self,
        question: str,
        session_id: str,
        user_id: int | None
    ):
        history = conversation_memory.get_history(session_id)
        try:
            result = await self.graph.ainvoke(
                {
                    "session_id": session_id,
                    "user_id": user_id,
                    "question": question,
                    "history": history,
                }
            )
            agent = result.get("route", "general")
            answer = result.get("answer", "")
            sources = result.get("sources")
        except Exception as exc:
            logger.exception(f"Agent 路由执行失败，回退到 general：{exc}")
            agent = "general"
            answer = await self.general_agent.run(question, history)
            sources = None

        conversation_memory.add_turn(session_id, question, answer)
        return AgentResponse(agent=agent, answer=answer, sources=sources)
