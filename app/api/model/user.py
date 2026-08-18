from pydantic import BaseModel, Field

class UserLoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=10, description="用户名")
    password: str = Field(..., min_length=3, max_length=12, description="密码")


class UserLoginResponse(BaseModel):
    user_id: int
    user_name: str
