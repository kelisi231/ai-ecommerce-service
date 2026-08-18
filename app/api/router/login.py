from fastapi import APIRouter, Depends
from app.api.model.user import UserLoginRequest, UserLoginResponse
from app.service.login import UserLoginService
from app.api.dependencies import user_login_service

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/login", response_model=UserLoginResponse)
async def login(
        login_data: UserLoginRequest,
        login_service: UserLoginService = Depends(user_login_service)
):
    result = await login_service.login(
        username=login_data.username,
        password=login_data.password
    )
    return result
