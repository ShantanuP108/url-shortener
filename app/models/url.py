import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from sqlalchemy.orm import relationship
from app.core.database import Base

class ShortURL(Base):
    __tablename__ = "short_urls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    short_code = Column(String(10), unique=True, index=True, nullable=False)
    target_url = Column(String, nullable=False)
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    owner = relationship("User", backref="urls")
