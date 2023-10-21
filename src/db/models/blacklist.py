from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from src.db.db import Base
import uuid

class Blacklist(Base):
    __tablename__ = "blacklist"
    email = Column(String, primary_key=True)
    app_uuid = Column(String)
    blocked_reason = Column(String)
