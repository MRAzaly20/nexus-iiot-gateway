from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class AnalyticsType(str, Enum):
    STATISTICS = "statistics"
    FFT = "fft"
    ANOMALY_DETECTION = "anomaly_detection"

# --- AnalyticsJob Models ---
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

# --- AnalyticsResult Models ---
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

# --- DataPoint Models (jika belum ada di data_processing.py) ---
class DataPointBase(BaseModel):
    timestamp: datetime
    tag_id: str
    value: float
    data_metadata: Optional[Dict[str, Any]] = None

class DataPointCreate(DataPointBase):
    pass

class DataPointUpdate(BaseModel):
    timestamp: Optional[datetime] = None
    tag_id: Optional[str] = None
    value: Optional[float] = None
    data_metadata: Optional[Dict[str, Any]] = None

class DataPointResponse(DataPointBase):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)