# models/event_alarm_db.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional
from ..databases import Base

# Enums untuk database
class AlarmSeverityEnum(str, PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlarmStateEnum(str, PyEnum):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    CLEARED = "cleared"

class TransformTypeEnum(str, PyEnum):
    NORMALIZE = "normalize"
    SCALE = "scale"
    UNIT_CONVERT = "unit_convert"
    FILTER = "filter"
    AGGREGATE = "aggregate"

class StorageTypeEnum(str, PyEnum):
    POSTGRES = "postgres"
    INFLUXDB = "influxdb"
    MONGODB = "mongodb"

class AnalyticsTypeEnum(str, PyEnum):
    STATISTICS = "statistics"
    FFT = "fft"
    ANOMALY_DETECTION = "anomaly_detection"

# --- Model untuk Event & Alarm Management ---

class AlarmRule(Base):
    __tablename__ = "alarm_rules"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    tag_id = Column(String(100), nullable=False, index=True)
    condition = Column(Text, nullable=False)  # Ekspresi logika, misal "value > 80"
    severity = Column(Enum(AlarmSeverityEnum), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class Alarm(Base):
    __tablename__ = "alarms"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    rule_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    tag_id = Column(String(100), nullable=False, index=True)
    severity = Column(Enum(AlarmSeverityEnum), nullable=False)
    timestamp_triggered = Column(DateTime(timezone=True), nullable=False, index=True)
    timestamp_cleared = Column(DateTime(timezone=True), nullable=True)
    state = Column(Enum(AlarmStateEnum), default=AlarmStateEnum.ACTIVE, nullable=False)
    value_at_trigger = Column(Float, nullable=False)
    acknowledged_by = Column(String(100))
    acknowledged_at = Column(DateTime(timezone=True))
    cleared_by = Column(String(100))
    cleared_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

# --- Model untuk Data Processing ---

class TransformFunction(Base):
    __tablename__ = "transform_functions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(Enum(TransformTypeEnum), nullable=False)
    parameters = Column(Text)  # JSON string untuk parameter
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class DataPoint(Base):
    __tablename__ = "data_points"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    tag_id = Column(String(100), nullable=False, index=True)
    value = Column(Float, nullable=False)
    metadata_json = Column(Text)  # JSON string untuk metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class ProcessedDataBatch(Base):
    __tablename__ = "processed_data_batches"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    batch_id = Column(String(100), unique=True, nullable=False, index=True)
    data_points_count = Column(Integer, nullable=False)
    processed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status = Column(String(50), default="completed", nullable=False)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

# --- Model untuk Buffering & Store-and-Forward ---

class BufferedDataEntry(Base):
    __tablename__ = "buffered_data_entrie"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    destination = Column(String(100), nullable=False, index=True)
    payload = Column(Text, nullable=False)
    timestamp_queued = Column(DateTime(timezone=True), nullable=False, index=True)
    retry_count = Column(Integer, default=0, nullable=False)
    max_retries = Column(Integer, default=3, nullable=False)
    status = Column(String(50), default="pending", nullable=False)
    last_attempt_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

# --- Model untuk TimeSeries Database Integration ---

class StorageConfig(Base):
    __tablename__ = "storage_config"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(255), nullable=False, unique=True)
    type = Column(Enum(StorageTypeEnum), nullable=False)
    connection_string = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    config_data = Column(Text)  # JSON string untuk konfigurasi tambahan
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

# --- Model untuk Edge Analytics ---

class AnalyticsJob(Base):
    __tablename__ = "analytics_jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(Enum(AnalyticsTypeEnum), nullable=False)
    input_tag_ids = Column(Text)  # JSON string untuk list tag IDs
    parameters = Column(Text)  # JSON string untuk parameter
    is_active = Column(Boolean, default=True, nullable=False)
    schedule = Column(String(100))
    last_run_at = Column(DateTime(timezone=True))
    next_run_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class AnalyticsResult(Base):
    __tablename__ = "analytics_results"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    job_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    result_data = Column(Text)  # JSON string untuk hasil
    execution_time_ms = Column(Integer)
    status = Column(String(50), default="success", nullable=False)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)