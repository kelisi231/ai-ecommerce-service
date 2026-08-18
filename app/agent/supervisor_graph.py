from typing import Literal, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph

from app.agent.general_agent import GeneralAgent
from app.agent.order_agent import OrderAgent
from app.agent.qa_agent import QAAgent
from app.api.model.rag import RAGSource

PLANNER_PROMPT = (
    "你是电商客服系统的意图分发器，负责把用户问题路由到正确的处理通道。\n"
    "候选通道：\n"
    "- qa: 商品信息、退换货政策、常见问题等知识库内容\n"
    "- order: 订单查询、订单状态、物流等与订单相关的问题\n"
    "- general: 闲聊寒暄、知识库之外的通用问题\n"
    "请结合历史对话判断用户当前问题的意图，调用 route_question 工具输出路由结果。"
)


@tool
def route_question(
        route: Literal["qa", "order", "general"],
        reason: str,
) -> str:
    """把用户问题路由到正确的处理通道。route 取值：qa=知识库问答（商品/政策/FAQ），order=订单查询，general=闲聊寒暄。"""
    return route


_ORDER_KEYWORDS = ("订单", "物流", "快递", "包裹", "发货", "收货", "配送", "到哪", "货运", "签收")
_QA_KEYWORDS = (
    "退货", "退款", "退换货", "换货", "优惠券", "积分", "发票",
    "政策", "保修", "质保", "价格", "热线", "客服", "售后", "到账",
)


def _parse_route(content) -> str:
    text = content.lower() if isinstance(content, str) else str(content)
    if any(k in text for k in _ORDER_KEYWORDS):
        return "order"
    if "order" in text:
        return "order"
    if any(k in text for k in _QA_KEYWORDS):
        return "qa"
    if "qa" in text:
        return "qa"
    return "general"


class AgentState(TypedDict, total=False):
    session_id: str
    user_id: int
    question: str
    history: list[BaseMessage]
    route: str
    answer: str
    sources: list[RAGSource] | None


def build_supervisor_graph(
        llm,
        qa_agent: QAAgent,
        order_agent: OrderAgent,
        general_agent: GeneralAgent,
):
    llm_with_route = llm.bind_tools([route_question])

    async def planner_node(state: AgentState):
        messages: list[BaseMessage] = [SystemMessage(content=PLANNER_PROMPT)]
        messages.extend(state.get("history") or [])
        messages.append(HumanMessage(content=f"用户问题：{state['question']}"))

        ai_message = await llm_with_route.ainvoke(messages)
        if ai_message.tool_calls:
            args = ai_message.tool_calls[0].get("args") or {}
            route = args.get("route")
            if route not in ("qa", "order", "general"):
                route = _parse_route(args.get("reason"))
        else:
            route = _parse_route(ai_message.content)
        return {"route": route}

    async def qa_node(state: AgentState):
        history = state.get("history") or []
        result = await qa_agent.run(state["question"], history)
        return {"answer": result.answer, "sources": result.sources}

    async def order_node(state: AgentState):
        if not state.get("user_id"):
            return {"answer": "查询订单需要先登录，请提供您的账号信息（user_id）后再试。"}
        history = state.get("history") or []
        answer = await order_agent.run(
            user_id=state["user_id"],
            question=state["question"],
            history=history,
        )

        return {"answer": answer}

    async def general_node(state: AgentState):
        history = state.get("history") or []
        answer = await general_agent.run(state["question"], history)
        return {"answer": answer}

    async def select_route(state: AgentState):
        return state.get("route", "general")

    graph = StateGraph(AgentState)
    graph.add_node("planner", planner_node)
    graph.add_node("qa", qa_node)
    graph.add_node("order", order_node)
    graph.add_node("general", general_node)

    graph.add_edge(START, "planner")
    graph.add_conditional_edges(
        "planner",
        select_route,
        {"qa": "qa", "order": "order", "general": "general"},
    )
    graph.add_edge("qa", END)
    graph.add_edge("order", END)
    graph.add_edge("general", END)
    return graph.compile()
