from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db import Base


class Page(Base):
    __tablename__ = "pages"
    __table_args__ = {"schema": "retail_copilot"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    cards = relationship("Card", back_populates="page", cascade="all, delete-orphan")
