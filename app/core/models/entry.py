from uuid import uuid4

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database import Base


class Entry(Base):
    __tablename__ = "entries"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    title = Column(String(64), nullable=True)
    body = Column(String(1024), nullable=True)
    created = Column(DateTime(timezone=True), nullable=True, server_default=func.now())
