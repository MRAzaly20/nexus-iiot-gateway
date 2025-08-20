from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from typing import Optional
from ..databases import Base

class BufferedDataEntry(Base):
    __tablename__ = "buffered_data_entries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    destination = Column(String(100), nullable=False, index=True)  # Identifier tujuan
    payload = Column(Text, nullable=False)  # Data yang diserialisasi (JSON)
    timestamp_queued = Column(DateTime(timezone=True), nullable=False, index=True)
    retry_count = Column(Integer, default=0, nullable=False)
    max_retries = Column(Integer, default=3, nullable=False)
    status = Column(String(50), default="pending", nullable=False)  # pending, processing, completed, failed
    last_attempt_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)