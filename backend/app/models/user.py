from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    google_id = Column(String(255), unique=True, index=True, nullable=True)
    # Optional password hash for email/password auth
    password_hash = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    tier = Column(String(20), default="free")  # free, pro
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
