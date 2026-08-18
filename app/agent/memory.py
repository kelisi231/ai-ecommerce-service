from collections import deque
import time

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
)


class ConversationMemory:
    """
    短期会话记忆:
    - 保存最近 N 轮对话
    - 超过 TTL 自动失效
    - 只保存用户消息和 AI 回复
    """

    def __init__(
            self,
            max_rounds: int = 10,
            ttl_seconds: int = 180,
    ):
        self.max_rounds = max_rounds
        self.ttl_seconds = ttl_seconds

        # session_id:
        # (
        #   messages,
        #   last_active_time
        # )
        self._sessions: dict[
            str,
            tuple[deque[BaseMessage], float]
        ] = {}

    def get_history(
            self,
            session_id: str,
    ) -> list[BaseMessage]:

        session = self._sessions.get(session_id)

        if session is None:
            return []

        messages, updated_at = session

        # 超过 TTL，删除上下文
        if time.time() - updated_at > self.ttl_seconds:
            self._sessions.pop(session_id, None)
            return []

        return list(messages)

    def add_turn(
            self,
            session_id: str,
            human_content: str,
            ai_content: str,
    ):

        session = self._sessions.get(session_id)

        now = time.time()

        if session is None:
            messages = deque(
                maxlen=self.max_rounds * 2
            )
        else:
            messages = session[0]

        messages.append(
            HumanMessage(
                content=human_content
            )
        )

        messages.append(
            AIMessage(
                content=ai_content
            )
        )

        self._sessions[session_id] = (
            messages,
            now
        )

        self._lazy_cleanup(now)

    def _lazy_cleanup(
            self,
            now: float,
    ) -> None:
        """删除过期 session，防止 _sessions 无限增长"""
        expired_sessions = [
            session_id
            for session_id, (_, updated_at) in self._sessions.items()
            if now - updated_at > self.ttl_seconds
        ]

        for session_id in expired_sessions:
            self._sessions.pop(
                session_id,
                None,
            )


conversation_memory = ConversationMemory()
