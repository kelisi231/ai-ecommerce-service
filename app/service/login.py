from app.repository.login import UserLoginRepository
from app.api.model.user import UserLoginResponse
from app.api.entity.user import User


class UserLoginService:
    def __init__(self, login_repository: UserLoginRepository):
        self.login_repository: UserLoginRepository = login_repository

    async def login(self, username: str, password: str):
        user: User | None = await self.login_repository.get_user_by_name(username)
        if not user:
            return None

        if password != user.password:
            return None

        return UserLoginResponse(
            user_id=user.user_id,
            user_name=user.username
        )
