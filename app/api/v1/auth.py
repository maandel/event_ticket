from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.auth import (
    AdminLoginRequest,
    LoginRequest,
    RegisterRequest,
)
from app.schemas.common import ApiResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", summary="User login")
async def login(
    request: Request,
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse:
    service = AuthService(db)
    data = await service.login(payload)
    return ApiResponse.ok(
        data=data.model_dump(),
        message="Login successful",
    )


@router.post("/register", status_code=201, summary="User registration")
async def register(
    request: Request,
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse:
    service = AuthService(db)
    data = await service.register(payload)
    return ApiResponse.ok(
        data=data.model_dump(),
        message="Account created successfully",
    )


@router.get("/me", summary="Get current user")
async def me(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ApiResponse:
    service = AuthService(db)
    data = await service.me(current_user)
    return ApiResponse.ok(data=data.model_dump())


@router.post("/admin/login", summary="Admin login")
async def admin_login(
    request: Request,
    payload: AdminLoginRequest,
    db: AsyncSession = Depends(get_db),
) -> ApiResponse:
    service = AuthService(db)
    data = await service.admin_login(payload)
    return ApiResponse.ok(
        data=data.model_dump(),
        message="Admin login successful",
    )
