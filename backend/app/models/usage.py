from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from app.core.database import Base

class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    fingerprint = Column(String(32), nullable=True, index=True)
    mode = Column(String(20), nullable=False)
    provider_used = Column(String(50), nullable=True)
    latency_ms = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
