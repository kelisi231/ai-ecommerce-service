from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.tools import tool

from app.service.order import OrderService

ORDER_SYSTEM_PROMPT = (
    "你是电商平台的订单查询助手，负责帮用户查询订单信息。\n"
    "请严格遵守以下要求：\n"
    "1. 只依据工具返回的真实订单数据回答，禁止编造订单；\n"
    "2. 用户询问订单列表时调用 get_orders，询问某个具体订单时调用 get_order_by_number；\n"
    "3. 如果查询不到订单，如实告知用户没有相关订单；\n"
    "4. 回答使用简体中文，简洁、口语化、友好。"
)


class OrderAgent:
    def __init__(self, order_service: OrderService, llm):
        self.order_service = order_service
        self.llm = llm

    def _build_tools(self, user_id: int):
        @tool
        async def get_orders() -> str:
            """查询当前用户的所有订单，返回订单号、状态、位置列表。"""
            orders = await self.order_service.get_orders(user_id)
            if not orders:
                return "该用户暂无订单。"
            return "\n".join(
                f"订单号：{o.order_num}，状态：{o.status_text}，位置：{o.position}"
                for o in orders
            )

        @tool
        async def get_order_by_number(order_num: str) -> str:
            """按订单号查询某个具体订单详情，参数 order_num 为订单号字符串。"""
            order = await self.order_service.get_order(order_num, user_id)
            if not order:
                return "未查询到该订单，请核对订单号是否正确。"
            return (
                f"订单号：{order.order_num}，状态：{order.status_text}，位置：{order.position}"
            )

        return [get_orders, get_order_by_number]

    async def run(
            self,
            user_id: int,
            question: str,
            history: list[BaseMessage] | None = None,
    ) -> str:
        tools = self._build_tools(user_id)
        llm_with_tools = self.llm.bind_tools(tools)

        messages: list[BaseMessage] = [SystemMessage(content=ORDER_SYSTEM_PROMPT)]
        if history:
            messages.extend(history)
        messages.append(HumanMessage(content=question))

        tool_map = {t.name: t for t in tools}
        for _ in range(3):
            ai_message = await llm_with_tools.ainvoke(messages)
            messages.append(ai_message)

            if not ai_message.tool_calls:
                content = ai_message.content
                return content if isinstance(content, str) else str(content)

            for tool_call in ai_message.tool_calls:
                selected = tool_map.get(tool_call["name"])
                if selected is None:
                    messages.append(
                        ToolMessage(content="未知工具", tool_call_id=tool_call["id"])
                    )
                    continue
                try:
                    result = await selected.ainvoke(tool_call["args"])
                    content = result if isinstance(result, str) else str(result)
                except Exception as exc:
                    content = f"工具执行出错：{exc}"
                messages.append(
                    ToolMessage(content=content, tool_call_id=tool_call["id"])
                )

        return "抱歉，我暂时无法处理您的请求，请稍后再试或联系人工客服。"
