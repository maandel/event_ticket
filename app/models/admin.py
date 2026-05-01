from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.mixins import TimestampMixin, generate_id
from app.db.session import Base


class Admin(Base, TimestampMixin):
    __tablename__ = "admins"

    id: Mapped[str] = mapped_column(
        String(32),
        primary_key=True,
        default=lambda: generate_id("adm"),
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    role: Mapped[str] = mapped_column(
        String(20),
        default="admin",
        nullable=False,
    )
