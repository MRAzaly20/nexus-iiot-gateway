# core/db_integrator.py
import logging
import asyncio
from typing import List, Dict, Any
from datetime import datetime

import asyncpg
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from pymongo import MongoClient

# Import dari schemas dan config
from ..models.data_processing import DataPointResponse, StorageConfigResponse, StorageType
from ..config import config

logger = logging.getLogger(__name__)

class DatabaseIntegrator:
    """
    Menangani integrasi dengan berbagai database time-series.
    """
    def __init__(self):
        self.postgres_pool = None
        self.influxdb_client = None
        self.mongodb_client = None
        # Konfigurasi aktif bisa disimpan di memori atau DB
        self.active_configs = {}  # Dict[StorageType, StorageConfigResponse]

    async def initialize(self):
        """Inisialisasi koneksi ke database."""
        try:
            # Inisialisasi PostgreSQL Pool
            if config.DATABASE_URL:
                self.postgres_pool = await asyncpg.create_pool(config.DATABASE_URL)
                logger.info("PostgreSQL pool created.")
            else:
                logger.warning("PostgreSQL DATABASE_URL not configured.")

            # Inisialisasi InfluxDB Client
            if config.INFLUXDB_URL and config.INFLUXDB_TOKEN and config.INFLUXDB_ORG:
                self.influxdb_client = InfluxDBClient(
                    url=config.INFLUXDB_URL, 
                    token=config.INFLUXDB_TOKEN, 
                    org=config.INFLUXDB_ORG
                )
                logger.info("InfluxDB client initialized.")
            else:
                logger.warning("InfluxDB configuration not complete.")

            # Inisialisasi MongoDB Client
            if config.MONGODB_URL:
                self.mongodb_client = MongoClient(config.MONGODB_URL)
                # Test connection
                self.mongodb_client.admin.command('ismaster')
                logger.info("MongoDB client initialized.")
            else:
                logger.warning("MongoDB MONGODB_URL not configured.")

        except Exception as e:
            logger.error(f"Error initializing database connections: {e}")
            raise

    async def write_to_postgres(self, data_points: List[Dict], config_data: Dict):
        """Menulis data points ke PostgreSQL."""
        if not self.postgres_pool:
            logger.error("PostgreSQL pool not initialized.")
            raise Exception("PostgreSQL pool not initialized.")

        # Asumsi tabel `ts_data` sudah dibuat:
        # CREATE TABLE ts_data (id SERIAL PRIMARY KEY, timestamp TIMESTAMPTZ NOT NULL, tag_id VARCHAR(255) NOT NULL, value DOUBLE PRECISION NOT NULL);
        insert_query = """
            INSERT INTO ts_data (timestamp, tag_id, value) SELECT * FROM unnest($1::timestamptz[], $2::text[], $3::double precision[])
        """
        try:
            # Konversi dictionary ke DataPointResponse untuk validasi
            validated_points = [DataPointResponse(**dp) for dp in data_points]
            
            timestamps = [dp.timestamp for dp in validated_points]
            tag_ids = [dp.tag_id for dp in validated_points]
            values = [dp.value for dp in validated_points]

            async with self.postgres_pool.acquire() as conn:
                await conn.execute(insert_query, timestamps, tag_ids, values)
            logger.info(f"Wrote {len(data_points)} points to PostgreSQL.")
        except Exception as e:
            logger.error(f"Error writing to PostgreSQL: {e}")
            raise

    def write_to_influxdb(self, data_points: List[Dict], config_data: Dict):
        """Menulis data points ke InfluxDB."""
        if not self.influxdb_client:
            logger.error("InfluxDB client not initialized.")
            raise Exception("InfluxDB client not initialized.")

        try:
            # Konversi dictionary ke DataPointResponse untuk validasi
            validated_points = [DataPointResponse(**dp) for dp in data_points]
            
            write_api = self.influxdb_client.write_api(write_options=SYNCHRONOUS)
            points = []
            
            for dp in validated_points:
                point = Point("measurement")\
                    .tag("tag_id", dp.tag_id)\
                    .field("value", dp.value)\
                    .time(dp.timestamp)
                points.append(point)
            
            # Ekstrak bucket dan org dari config_data atau gunakan default
            bucket = config_data.get('bucket') or config.INFLUXDB_BUCKET
            org = config_data.get('org') or config.INFLUXDB_ORG
            
            write_api.write(bucket=bucket, org=org, record=points)
            logger.info(f"Wrote {len(points)} points to InfluxDB.")
        except Exception as e:
            logger.error(f"Error writing to InfluxDB: {e}")
            raise

    def write_to_mongodb(self, data_points: List[Dict], config_data: Dict):
        """Menulis data points ke MongoDB."""
        if not self.mongodb_client:
            logger.error("MongoDB client not initialized.")
            raise Exception("MongoDB client not initialized.")

        try:
            # Konversi dictionary ke DataPointResponse untuk validasi
            validated_points = [DataPointResponse(**dp) for dp in data_points]
            
            db = self.mongodb_client[config.MONGODB_DB_NAME]
            collection = db["ts_data"]
            docs = [
                {
                    "timestamp": dp.timestamp,
                    "tag_id": dp.tag_id,
                    "value": dp.value,
                    "created_at": datetime.now()
                } 
                for dp in validated_points
            ]
            result = collection.insert_many(docs)
            logger.info(f"Wrote {len(result.inserted_ids)} points to MongoDB.")
        except Exception as e:
            logger.error(f"Error writing to MongoDB: {e}")
            raise

    async def write_data(self, data_points: List[Dict], storage_config: Dict):
        """Routing tulis data berdasarkan tipe storage."""
        try:
            # Validasi storage config
            config_obj = StorageConfigResponse(**storage_config)
            
            if config_obj.type == StorageType.POSTGRES:
                await self.write_to_postgres(data_points, storage_config)
            elif config_obj.type == StorageType.INFLUXDB:
                # InfluxDB write adalah synchronous
                await asyncio.get_event_loop().run_in_executor(
                    None, self.write_to_influxdb, data_points, storage_config
                )
            elif config_obj.type == StorageType.MONGODB:
                # MongoDB write adalah synchronous
                await asyncio.get_event_loop().run_in_executor(
                    None, self.write_to_mongodb, data_points, storage_config
                )
            else:
                error_msg = f"Unsupported storage type: {config_obj.type}"
                logger.warning(error_msg)
                raise ValueError(error_msg)
                
        except Exception as e:
            logger.error(f"Failed to write data to {storage_config.get('type', 'unknown')}: {e}")
            # Di sini Anda bisa memicu buffering jika penulisan gagal
            raise

    async def close(self):
        """Menutup semua koneksi database."""
        try:
            # Tutup PostgreSQL pool
            if self.postgres_pool:
                await self.postgres_pool.close()
                logger.info("PostgreSQL pool closed.")

            # Tutup InfluxDB client
            if self.influxdb_client:
                self.influxdb_client.close()
                logger.info("InfluxDB client closed.")

            # Tutup MongoDB client
            if self.mongodb_client:
                self.mongodb_client.close()
                logger.info("MongoDB client closed.")
                
        except Exception as e:
            logger.error(f"Error closing database connections: {e}")

    def parse_connection_string(self, connection_string: str) -> Dict[str, str]:
        """Parse connection string menjadi dictionary parameter."""
        try:
            params = {}
            if ';' in connection_string:
                # Format: key1=value1;key2=value2
                pairs = connection_string.split(';')
                for pair in pairs:
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        params[key.strip()] = value.strip()
            elif '://' in connection_string:
                # Format URL
                params['url'] = connection_string
            return params
        except Exception as e:
            logger.error(f"Error parsing connection string: {e}")
            return {}