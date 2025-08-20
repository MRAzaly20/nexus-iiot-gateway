# models.py
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any, Union
from enum import Enum
from datetime import datetime
# --- Model untuk Data Processing ---
# ... (definisi enum dan model lainnya) ...

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

class Alarm(BaseModel):
    model_config = ConfigDict(
        # from_attributes=True, # Berguna jika membuat model dari ORM object
        json_encoders={ # Cara lama, tapi masih didukung
            datetime: lambda v: v.isoformat() # Konversi datetime ke string ISO
        }
    )
    id: Optional[str] = None
    rule_id: str
    name: str
    description: Optional[str] = None
    tag_id: str
    severity: AlarmSeverity # Diambil dari rule
    # --- PERUBAHAN DI SINI ---
    timestamp_triggered: datetime # <-- Gunakan tipe datetime, bukan str
    timestamp_cleared: Optional[datetime] = None # <-- Gunakan tipe datetime, bukan str
    # --- AKHIR PERUBAHAN ---
    state: AlarmState = AlarmState.ACTIVE
  
class TransformType(str, Enum):
    NORMALIZE = "normalize"
    SCALE = "scale"
    UNIT_CONVERT = "unit_convert"
    FILTER = "filter"
    AGGREGATE = "aggregate"

class TransformFunction(BaseModel):
    id: Optional[str] = None
    name: str # Nama fungsi, misal "Scale to Celsius"
    type: TransformType
    parameters: Dict[str, Any] # Parameter spesifik untuk transformasi
    # Contoh untuk scale: {"input_min": 0, "input_max": 100, "output_min": 0, "output_max": 1000}

class DataPoint(BaseModel):
    timestamp: str # ISO format
    tag_id: str
    value: float
    # Metadata tambahan bisa ditambahkan

class ProcessedDataBatch(BaseModel):
    batch_id: str
    data_points: List[DataPoint]

# --- Model untuk Buffering & Store-and-Forward ---
class BufferedDataEntry(BaseModel):
    id: Optional[str] = None # ID unik untuk entry buffer
    destination: str # Identifier tujuan (e.g., "cloud_aws", "influxdb_local")
    payload: str # Data yang diserialisasi (JSON)
    timestamp_queued: str # ISO format
    retry_count: int = 0

# --- Model untuk TimeSeries Database Integration ---
class StorageType(str, Enum):
    POSTGRES = "postgres"
    INFLUXDB = "influxdb"
    MONGODB = "mongodb"

class StorageConfig(BaseModel):
    id: Optional[str] = None
    name: str
    type: StorageType
    connection_string: str # URL atau parameter koneksi
    is_active: bool = True
    # Parameter spesifik lainnya bisa ditambahkan berdasarkan tipe

# --- Model untuk Event & Alarm Management ---
class AlarmSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlarmRule(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    # Format kondisi bisa lebih kompleks, ini versi sederhana
    tag_id: str # ID tag yang dimonitor
    condition: str # Ekspresi logika, misal "value > 80"
    severity: AlarmSeverity
    is_active: bool = True
    # Notifikasi bisa ditambahkan di sini atau di model terpisah

class AlarmState(str, Enum):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    CLEARED = "cleared"

class Alarm(BaseModel):
    id: Optional[str] = None
    rule_id: str
    name: str # Diambil dari rule
    description: Optional[str] # Diambil dari rule
    tag_id: str
    severity: AlarmSeverity # Diambil dari rule
    timestamp_triggered: str # ISO format
    timestamp_cleared: Optional[str] = None # ISO format
    state: AlarmState = AlarmState.ACTIVE
    value_at_trigger: float # Nilai tag saat alarm dipicu

# --- Model untuk Edge Analytics ---
class AnalyticsType(str, Enum):
    STATISTICS = "statistics"
    FFT = "fft"
    ANOMALY_DETECTION = "anomaly_detection"

class AnalyticsJob(BaseModel):
    id: Optional[str] = None
    name: str
    type: AnalyticsType
    # Parameter untuk job analytics
    input_tag_ids: List[str] # Tag yang akan dianalisis
    parameters: Dict[str, Any] # Parameter spesifik, e.g., window_size untuk stats
    is_active: bool = True

class AnalyticsResult(BaseModel):
    job_id: str
    timestamp: str # ISO format
    result_data: Dict[str, Any] # Hasil spesifik tergantung tipe analisis
