import os
from typing import Optional

class Config:
    # --- Konfigurasi Database ---

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "Administrator1234")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "iiot_data")
    
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    DATABASE_URL_ASYN: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    
    # --- Konfigurasi Redis ---
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB_BUFFER: int = int(os.getenv("REDIS_DB_BUFFER", 1))
    REDIS_DB_CACHE: int = int(os.getenv("REDIS_DB_CACHE", 0))
    
    # --- Konfigurasi InfluxDB ---
    INFLUXDB_URL: str = os.getenv("INFLUXDB_URL", "http://localhost:8086")
    INFLUXDB_TOKEN: str = os.getenv("INFLUXDB_TOKEN", "my-token")
    INFLUXDB_ORG: str = os.getenv("INFLUXDB_ORG", "my-org")
    INFLUXDB_BUCKET: str = os.getenv("INFLUXDB_BUCKET", "my-bucket")
    
    # --- Konfigurasi MongoDB ---
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "iiot_ts")

config = Config()