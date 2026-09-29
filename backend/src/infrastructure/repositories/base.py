from typing import Generic, TypeVar, Type, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.models.base import Base

T = TypeVar("T", bound=Base)

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession, enterprise_id: UUID):
        self.model = model
        self.session = session
        self.enterprise_id = enterprise_id

    async def get_by_id(self, id: UUID) -> Optional[T]:
        query = select(self.model).where(
            self.model.id == id,
            self.model.enterprise_id == self.enterprise_id
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()