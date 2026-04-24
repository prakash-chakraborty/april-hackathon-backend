from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class Card(Base):
    __tablename__ = "cards"
    __table_args__ = {"schema": "retail_copilot"}

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("retail_copilot.pages.id"), nullable=False)
    title = Column(String(200), nullable=False)
    card_type = Column(String(50), nullable=False)
    metric_title = Column(String(200), nullable=False)
    metric_value = Column(String(200), nullable=False)

    page = relationship("Page", back_populates="cards")
