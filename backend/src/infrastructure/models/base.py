import uuid
from datetime import datetime, UTC
from sqlalchemy import DateTime, Uuid, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(UTC), 
        onupdate=lambda: datetime.now(UTC)
    )

class OptimisticMixin:
    version_id: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    __mapper_args__ = {
        "version_id_col": version_id
    }

class TenantMixin:
    @declared_attr
    def enterprise_id(cls) -> Mapped[uuid.UUID]:
        return mapped_column(Uuid, ForeignKey("enterprises.id"), nullable=False, index=True)