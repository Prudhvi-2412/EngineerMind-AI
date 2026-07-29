from datetime import datetime, timezone
from typing import Optional, Dict, Any
import uuid
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, UniqueConstraint, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from app.infrastructure.persistence.postgres.models.base import Base


class EngineeringEventModel(Base):
    __tablename__ = "engineering_events"
    __table_args__ = (
        UniqueConstraint("event_id", name="uq_engineering_events_delivery_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True, index=True)
    repo_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("repositories.id", ondelete="SET NULL"), nullable=True, index=True)
    event_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)  # X-GitHub-Delivery GUID
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)            # push, pull_request.opened, etc.
    source: Mapped[str] = mapped_column(String(50), nullable=False, default="github")
    payload: Mapped[Dict[str, Any]] = mapped_column(JSON().with_variant(JSONB, "postgresql"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="RECEIVED", index=True) # RECEIVED, PROCESSING, PROCESSED, FAILED
    retry_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
