from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class PromptHistory(Base):
    __tablename__ = "prompt_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    original_prompt = Column(Text, nullable=False)
    enhanced_prompt = Column(Text, nullable=True)
    mode = Column(String(20), nullable=False)
    provider_used = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
