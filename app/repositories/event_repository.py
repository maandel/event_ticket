from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event, Section


class EventRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, event_id: str) -> Event | None:
        result = await self.db.execute(
            select(Event).where(
                Event.id == event_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_events(
        self,
        search: str | None,
        location: str | None,
        team: str | None,
        stage: str | None,
        price_min: float | None,
        price_max: float | None,
        page: int,
        limit: int,
    ) -> tuple[list[Event], int]:
        stmt = select(Event)
        filters = []

        if search:
            ilike = f"%{search}%"
            filters.append(
                or_(
                    Event.title.ilike(ilike),
                    Event.venue.ilike(ilike),
                    Event.city.ilike(ilike),
                )
            )

        if location:
            ilike = f"%{location}%"
            filters.append(
                or_(
                    Event.city.ilike(ilike),
                    Event.country.ilike(ilike),
                )
            )

        if stage:
            filters.append(Event.stage.ilike(f"%{stage}%"))

        if price_min is not None:
            filters.append(Event.price_min >= price_min)

        if price_max is not None:
            filters.append(Event.price_max <= price_max)

        if filters:
            stmt = stmt.where(and_(*filters))

        if team:
            stmt = stmt.where(
                Event.teams.cast(type_=None).astext.ilike(f"%{team}%"),
            )

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar_one()

        stmt = (
            stmt.order_by(Event.created_at.desc())
            .offset((page - 1) * limit)
            .limit(
                limit,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all(), total

    async def create(self, **kwargs) -> Event:
        event = Event(**kwargs)
        self.db.add(event)
        await self.db.flush()
        await self.db.refresh(event)
        return event

    async def update(self, event: Event, updates: dict) -> Event:
        for key, value in updates.items():
            setattr(event, key, value)
        await self.db.flush()
        await self.db.refresh(event)
        return event

    async def delete(self, event: Event) -> None:
        await self.db.delete(event)
        await self.db.flush()


class SectionRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, section_id: str) -> Section | None:
        result = await self.db.execute(
            select(Section).where(
                Section.id == section_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_by_event(self, event_id: str) -> list[Section]:
        result = await self.db.execute(
            select(Section)
            .where(Section.event_id == event_id)
            .order_by(
                Section.price.desc(),
            )
        )
        return result.scalars().all()

    async def create(self, **kwargs) -> Section:
        section = Section(**kwargs)
        self.db.add(section)
        await self.db.flush()
        await self.db.refresh(section)
        return section

    async def update(self, section: Section, updates: dict) -> Section:
        for key, value in updates.items():
            setattr(section, key, value)
        await self.db.flush()
        await self.db.refresh(section)
        return section

    async def delete(self, section: Section) -> None:
        await self.db.delete(section)
        await self.db.flush()
