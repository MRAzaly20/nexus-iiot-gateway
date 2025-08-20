from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any, Union
from enum import Enum
from datetime import datetime

# --- Model untuk Event & Alarm Management ---

class AlarmSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlarmState(str, Enum):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    CLEARED = "cleared"

class AlarmRuleBase(BaseModel):
    name: str
    description: Optional[str] = None
    tag_id: str
    condition: str
    severity: AlarmSeverity
    is_active: bool = True

class AlarmRuleCreate(AlarmRuleBase):
    pass

class AlarmRuleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    tag_id: Optional[str] = None
    condition: Optional[str] = None
    severity: Optional[AlarmSeverity] = None
    is_active: Optional[bool] = None

class AlarmRuleResponse(AlarmRuleBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AlarmRule(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    # Format kondisi bisa lebih kompleks, ini versi sederhana
    tag_id: str # ID tag yang dimonitor
    condition: str # Ekspresi logika, misal "value > 80"
    severity: AlarmSeverity
    is_active: bool = True
    
class AlarmBase(BaseModel):
    rule_id: str
    name: str
    description: Optional[str] = None
    tag_id: str
    severity: AlarmSeverity
    value_at_trigger: float
    state: AlarmState = AlarmState.ACTIVE

class AlarmCreateRequest(BaseModel):
    rule_id: str
    name: str
    description: Optional[str] = None
    tag_id: str
    severity: AlarmSeverity
    timestamp_triggered: Optional[datetime] = None
    state: AlarmState = AlarmState.ACTIVE
    value_at_trigger: float

class AlarmUpdate(BaseModel):
    rule_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    tag_id: Optional[str] = None
    severity: Optional[AlarmSeverity] = None
    timestamp_cleared: Optional[datetime] = None
    state: Optional[AlarmState] = None
    value_at_trigger: Optional[float] = None
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    cleared_by: Optional[str] = None

class AlarmResponse(AlarmBase):
    id: str
    rule_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    tag_id: Optional[str] = None
    severity: Optional[AlarmSeverity] = None
    timestamp_triggered: datetime
    timestamp_cleared: Optional[datetime] = None
    state: Optional[AlarmState] = None
    value_at_trigger: Optional[float] = None
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    cleared_by: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# --- Model untuk Data Processing ---
class TransformType(str, Enum):
    NORMALIZE = "normalize"
    SCALE = "scale"
    UNIT_CONVERT = "unit_convert"
    FILTER = "filter"
    AGGREGATE = "aggregate"

class TransformFunctionBase(BaseModel):
    name: str
    type: TransformType
    parameters: Optional[Dict[str, Any]] = None
    is_active: bool = True

class TransformFunctionCreate(TransformFunctionBase):
    pass

class TransformFunctionUpdate(TransformFunctionBase):
    name: Optional[str] = None
    type: Optional[TransformType] = None
    is_active: Optional[bool] = None

class TransformFunctionResponse(TransformFunctionBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DataPointBase(BaseModel):
    timestamp: datetime
    tag_id: str
    value: float
    metadata: Optional[Dict[str, Any]] = None

class DataPointCreate(DataPointBase):
    pass

class DataPointResponse(DataPointBase):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProcessedDataBatchBase(BaseModel):
    batch_id: str
    data_points_count: int
    status: str = "completed"
    error_message: Optional[str] = None

class ProcessedDataBatchCreate(ProcessedDataBatchBase):
    pass

class ProcessedDataBatchResponse(ProcessedDataBatchBase):
    id: str
    processed_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- Model untuk Buffering & Store-and-Forward ---
class BufferedDataEntryBase(BaseModel):
    destination: str
    payload: str
    timestamp_queued: datetime
    retry_count: int = 0
    max_retries: int = 3
    status: str = "pending"
    last_attempt_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

class BufferedDataEntryCreate(BufferedDataEntryBase):
    pass

class BufferedDataEntryResponse(BufferedDataEntryBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- Model untuk TimeSeries Database Integration ---
class StorageType(str, Enum):
    POSTGRES = "postgres"
    INFLUXDB = "influxdb"
    MONGODB = "mongodb"

class StorageConfigBase(BaseModel):
    name: str
    type: StorageType
    connection_string: str
    is_active: bool = True
    config_data: Optional[str] = None

class StorageConfigCreate(StorageConfigBase):
    pass

class StorageConfigUpdate(StorageConfigBase):
    name: Optional[str] = None
    type: Optional[StorageType] = None
    connection_string: Optional[str] = None
    is_active: Optional[bool] = None

class StorageConfigResponse(StorageConfigBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- Model untuk Edge Analytics ---
class AnalyticsType(str, Enum):
    STATISTICS = "statistics"
    FFT = "fft"
    ANOMALY_DETECTION = "anomaly_detection"

class AnalyticsJobBase(BaseModel):
    name: str
    type: AnalyticsType
    input_tag_ids: Optional[List[str]] = None
    parameters: Optional[Dict[str, Any]] = None
    is_active: bool = True
    schedule: Optional[str] = None

class AnalyticsJobCreate(AnalyticsJobBase):
    pass

class AnalyticsJobUpdate(AnalyticsJobBase):
    name: Optional[str] = None
    type: Optional[AnalyticsType] = None
    is_active: Optional[bool] = None

class AnalyticsJobResponse(AnalyticsJobBase):
    id: str
    last_run_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AnalyticsResultBase(BaseModel):
    job_id: str
    timestamp: datetime
    result_data: Optional[Dict[str, Any]] = None
    execution_time_ms: Optional[int] = None
    status: str = "success"
    error_message: Optional[str] = None

class AnalyticsResultCreate(AnalyticsResultBase):
    pass

class AnalyticsResultResponse(AnalyticsResultBase):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)