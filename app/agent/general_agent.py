from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

GENERAL_SYSTEM_PROMPT = (
    "你是电商平台的智能客服助手，负责与用户进行日常闲聊、寒暄以及知识库之外的通用问题。\n"
    "请严格遵守以下要求：\n"
    "1. 回答使用简体中文，语气友好、亲切；\n"
    "2. 只回答力所能及的问题，不编造事实，不承诺平台未提供的服务；\n"
    "3. 涉及商品、政策、订单等专业问题时，建议用户转接对应渠道。"
)


class GeneralAgent:
    def __init__(self, llm):
        self.llm = llm

    async def run(self, question: str, history: list[BaseMessage] | None = None) -> str:
        messages: list[BaseMessage] = [SystemMessage(content=GENERAL_SYSTEM_PROMPT)]
        if history:
            messages.extend(history)
        messages.append(HumanMessage(content=question))

        resp = await self.llm.ainvoke(messages)
        return resp.content if isinstance(resp.content, str) else str(resp.content)