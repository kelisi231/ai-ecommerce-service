from sqlalchemy import text

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.api.entity.user import User


class UserLoginRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user_by_name(self, username: str) -> User | None:
        sql = text("SELECT user_id, username, password FROM user WHERE username = :username")
        result = await self.session.execute(sql, {"username": username})
        row = result.mappings().first()

        if not row:
            return None

        return User(
            user_id=row['user_id'],
            username=row['username'],
            password=row['password']
        )
