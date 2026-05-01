from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, UnauthorizedError
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.repositories.admin_repository import AdminRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    AdminLoginRequest,
    AdminLoginResponse,
    AdminOut,
    LoginRequest,
    LoginResponse,
    MeResponse,
    RegisterRequest,
    UserOut,
)


class AuthService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.user_repo = UserRepository(db)
        self.admin_repo = AdminRepository(db)

    async def login(self, payload: LoginRequest) -> LoginResponse:
        user = await self.user_repo.get_by_email(payload.email)
        if not user or not verify_password(
            payload.password,
            user.hashed_password,
        ):
            raise UnauthorizedError("Invalid email or password")
        token = create_access_token(
            subject=user.id,
            extra_claims={"role": user.role},
        )
        return LoginResponse(token=token, user=UserOut.from_orm_model(user))

    async def register(self, payload: RegisterRequest) -> LoginResponse:
        existing = await self.user_repo.get_by_email(payload.email)
        if existing:
            raise ConflictError("An account with this email already exists")
        user = await self.user_repo.create(
            email=payload.email,
            hashed_password=hash_password(payload.password),
            first_name=payload.first_name,
            last_name=payload.last_name,
            phone=payload.phone,
            country_code=payload.country_code,
        )
        token = create_access_token(
            subject=user.id,
            extra_claims={"role": user.role},
        )
        return LoginResponse(token=token, user=UserOut.from_orm_model(user))

    async def me(self, user) -> MeResponse:
        return MeResponse(user=UserOut.from_orm_model(user))

    async def admin_login(
        self,
        payload: AdminLoginRequest,
    ) -> AdminLoginResponse:
        admin = await self.admin_repo.get_by_email(payload.email)
        if not admin or not verify_password(
            payload.password,
            admin.hashed_password,
        ):
            raise UnauthorizedError("Invalid email or password")
        token = create_access_token(
            subject=admin.id,
            extra_claims={"role": "admin"},
        )
        return AdminLoginResponse(
            token=token,
            admin=AdminOut.from_orm_model(admin),
        )
