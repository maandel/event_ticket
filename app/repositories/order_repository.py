from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order


class OrderRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, order_id: str) -> Order | None:
        result = await self.db.execute(
            select(Order).where(
                Order.id == order_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_by_stripe_intent(self, intent_id: str) -> Order | None:
        result = await self.db.execute(
            select(Order).where(Order.stripe_payment_intent_id == intent_id)
        )
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: str,
        status: str | None,
        page: int,
        limit: int,
    ) -> tuple[list[Order], int]:
        from sqlalchemy import func

        filters = [Order.user_id == user_id]
        if status:
            filters.append(Order.status == status)

        stmt = select(Order).where(and_(*filters))
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self.db.execute(count_stmt)).scalar_one()

        stmt = (
            stmt.order_by(Order.created_at.desc())
            .offset((page - 1) * limit)
            .limit(
                limit,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all(), total

    async def list_all(
        self,
        status: str | None,
        event_id: str | None,
        page: int,
        limit: int,
    ) -> tuple[list[Order], int]:
        from sqlalchemy import func

        filters = []
        if status:
            filters.append(Order.status == status)
        if event_id:
            filters.append(Order.event_id == event_id)

        stmt = select(Order)
        if filters:
            stmt = stmt.where(and_(*filters))

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self.db.execute(count_stmt)).scalar_one()

        stmt = (
            stmt.order_by(Order.created_at.desc())
            .offset((page - 1) * limit)
            .limit(
                limit,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all(), total

    async def create(self, **kwargs) -> Order:
        order = Order(**kwargs)
        self.db.add(order)
        await self.db.flush()
        await self.db.refresh(order)
        return order

    async def update_status(self, order: Order, status: str) -> Order:
        order.status = status
        await self.db.flush()
        await self.db.refresh(order)
        return order
