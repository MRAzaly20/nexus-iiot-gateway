from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from enum import Enum
from typing import Optional
from ..databases import Base

class StorageType(str, Enum):
    POSTGRES = "postgres"
    INFLUXDB = "influxdb"
    MONGODB = "mongodb"

class StorageConfig(Base):
    __tablename__ = "storage_configs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(255), nullable=False, unique=True)
    type = Column(String(50), nullable=False)  # StorageType enum
    connection_string = Column(Text, nullable=False)  # URL atau parameter koneksi
    is_active = Column(Boolean, default=True, nullable=False)
    config_data = Column(Text)  # JSON string untuk konfigurasi tambahan
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)