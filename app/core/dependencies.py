from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import decode_token
from app.db.session import get_db
from app.repositories.user_repository import UserRepository

bearer_scheme = HTTPBearer(auto_error=False)


async def _get_token_payload(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict:
    if not credentials:
        raise UnauthorizedError("Authentication token is missing")
    try:
        payload = decode_token(credentials.credentials)
    except JWTError:
        raise UnauthorizedError("Invalid or expired token")
    if payload.get("type") != "access":
        raise UnauthorizedError("Invalid token type")
    return payload


async def get_current_user(
    payload: dict = Depends(_get_token_payload),
    db: AsyncSession = Depends(get_db),
):
    user_id: str | None = payload.get("sub")
    if not user_id:
        raise UnauthorizedError()
    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)
    if not user:
        raise UnauthorizedError("User not found")
    return user


async def get_current_admin(
    payload: dict = Depends(_get_token_payload),
    db: AsyncSession = Depends(get_db),
):
    from app.repositories.admin_repository import AdminRepository

    if payload.get("role") != "admin":
        raise ForbiddenError("Admin access required")
    admin_id: str | None = payload.get("sub")
    if not admin_id:
        raise UnauthorizedError()
    repo = AdminRepository(db)
    admin = await repo.get_by_id(admin_id)
    if not admin:
        raise UnauthorizedError("Admin not found")
    return admin


async def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
):
    if not credentials:
        return None
    try:
        payload = decode_token(credentials.credentials)
    except JWTError:
        return None
    if payload.get("type") != "access" or payload.get("role") == "admin":
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    repo = UserRepository(db)
    return await repo.get_by_id(user_id)
