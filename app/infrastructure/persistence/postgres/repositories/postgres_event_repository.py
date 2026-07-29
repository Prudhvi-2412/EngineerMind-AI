from datetime import datetime, timezone
from typing import Optional, List
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.domain.entities.engineering_event import EngineeringEvent
from app.infrastructure.persistence.postgres.models.engineering_event_model import EngineeringEventModel


class PostgresEventRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_event(self, entity: EngineeringEvent) -> EngineeringEventModel:
        model = EngineeringEventModel(
            id=entity.id,
            org_id=entity.org_id,
            repo_id=entity.repo_id,
            event_id=entity.event_id,
            event_type=entity.event_type,
            source=entity.source,
            payload=entity.payload,
            status=entity.status,
            retry_count=entity.retry_count,
            created_at=entity.created_at
        )
        self.session.add(model)
        await self.session.flush()
        return model

    async def get_by_delivery_id(self, event_id: str) -> Optional[EngineeringEventModel]:
        stmt = select(EngineeringEventModel).where(EngineeringEventModel.event_id == event_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_id(self, id: uuid.UUID) -> Optional[EngineeringEventModel]:
        stmt = select(EngineeringEventModel).where(EngineeringEventModel.id == id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def update_status(
        self,
        event_uuid: uuid.UUID,
        status: str,
        error_message: Optional[str] = None,
        retry_count: Optional[int] = None
    ) -> None:
        values = {
            "status": status,
            "processed_at": datetime.now(timezone.utc) if status in ("PROCESSED", "FAILED") else None
        }
        if error_message is not None:
            values["error_message"] = error_message
        if retry_count is not None:
            values["retry_count"] = retry_count

        stmt = update(EngineeringEventModel).where(EngineeringEventModel.id == event_uuid).values(**values)
        await self.session.execute(stmt)
        await self.session.flush()

    async def list_failed_events(self, limit: int = 50) -> List[EngineeringEventModel]:
        stmt = select(EngineeringEventModel).where(EngineeringEventModel.status == "FAILED").limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
