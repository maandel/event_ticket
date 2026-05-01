from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admin import Admin


class AdminRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, admin_id: str) -> Admin | None:
        result = await self.db.execute(
            select(Admin).where(
                Admin.id == admin_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Admin | None:
        result = await self.db.execute(
            select(Admin).where(
                Admin.email == email.lower().strip(),
            )
        )
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> Admin:
        if "email" in kwargs:
            kwargs["email"] = kwargs["email"].lower().strip()
        admin = Admin(**kwargs)
        self.db.add(admin)
        await self.db.flush()
        await self.db.refresh(admin)
        return admin
