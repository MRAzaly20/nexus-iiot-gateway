# core/alarm_manager.py
import logging
import redis
import asyncpg
import json
from typing import List, Optional, Dict, Any
from datetime import datetime
import asyncio

# Import dari schemas dan config
from ..models.event_alarm import AlarmResponse, AlarmState, AlarmSeverity
from ..config import config

logger = logging.getLogger(__name__)

class AlarmManager:
    """
    Mengelola status alarm: menyimpan, memperbarui, mengakkses.
    Menggunakan PostgreSQL untuk penyimpanan persisten dan Redis untuk cache.
    """
    def __init__(self):
        self.db_pool: Optional[asyncpg.Pool] = None
        self.redis_client: Optional[redis.Redis] = None
        self.cache_ttl = 300  # Cache timeout dalam detik (5 menit)

    async def initialize(self):
        """Inisialisasi koneksi database dan Redis."""
        try:
            # Inisialisasi pool koneksi PostgreSQL
            if config.DATABASE_URL:
                self.db_pool = await asyncpg.create_pool(config.DATABASE_URL)
                logger.info("PostgreSQL pool for AlarmManager created.")
            else:
                logger.warning("PostgreSQL DATABASE_URL not configured.")

            # Inisialisasi koneksi Redis untuk cache
            if config.REDIS_HOST and config.REDIS_PORT:
                self.redis_client = redis.Redis(
                    host=config.REDIS_HOST, 
                    port=config.REDIS_PORT, 
                    db=config.REDIS_DB_CACHE, 
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_timeout=5,
                    retry_on_timeout=True
                )
                # Test koneksi Redis
                self.redis_client.ping()
                logger.info("Redis client for AlarmManager cache initialized.")
            else:
                logger.warning("Redis configuration not complete.")

            # Buat tabel jika belum ada (sekali saja saat startup)
            if self.db_pool:
                await self._create_tables_if_not_exist()

        except Exception as e:
            logger.error(f"Error initializing AlarmManager connections: {e}")
            raise

    async def _create_tables_if_not_exist(self):
        """Membuat tabel alarm jika belum ada."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS alarms (
            id TEXT PRIMARY KEY,
            rule_id TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            tag_id TEXT NOT NULL,
            severity TEXT NOT NULL,
            timestamp_triggered TIMESTAMPTZ NOT NULL,
            timestamp_cleared TIMESTAMPTZ,
            state TEXT NOT NULL DEFAULT 'active',
            value_at_trigger DOUBLE PRECISION NOT NULL,
            acknowledged_by TEXT,
            acknowledged_at TIMESTAMPTZ,
            cleared_by TEXT,
            cleared_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS idx_alarms_state ON alarms(state);
        CREATE INDEX IF NOT EXISTS idx_alarms_timestamp ON alarms(timestamp_triggered DESC);
        CREATE INDEX IF NOT EXISTS idx_alarms_rule_id ON alarms(rule_id);
        CREATE INDEX IF NOT EXISTS idx_alarms_tag_id ON alarms(tag_id);
        """
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute(create_table_query)
            logger.info("Alarm table ensured to exist.")
        except Exception as e:
            logger.error(f"Error creating alarm table: {e}")
            raise

    async def add_alarms(self, alarms: List[Dict]) -> bool:
        """Menambahkan alarm baru yang terpicu ke database dan cache."""
        if not self.db_pool:
            error_msg = "Database pool not initialized in AlarmManager."
            logger.error(error_msg)
            raise Exception(error_msg)

        insert_query = """
        INSERT INTO alarms (
            id, rule_id, name, description, tag_id, severity, 
            timestamp_triggered, timestamp_cleared, state, value_at_trigger,
            acknowledged_by, acknowledged_at, cleared_by
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
        """
        # print(alarms)  # Debugging: Print the alarms data being processed
        try:
            # Validasi dan konversi alarm data
            validated_alarms = []
            for alarm_dict in alarms:
                print(alarm_dict)  # Debugging: Print each alarm dictionary
                try:
                    # Validasi dengan Pydantic model
                    alarm = AlarmResponse(**alarm_dict)
                    validated_alarms.append(alarm)
                except Exception as e:
                    logger.warning(f"Invalid alarm data skipped: {e}")
                    continue

            if not validated_alarms:
                logger.warning("No valid alarms to add.")
                return False

            records = []
            for alarm in validated_alarms:
                record = (
                    alarm.id,
                    alarm.rule_id,
                    alarm.name,
                    alarm.description,
                    alarm.tag_id,
                    alarm.severity.value if isinstance(alarm.severity, AlarmSeverity) else str(alarm.severity),
                    alarm.timestamp_triggered,
                    alarm.timestamp_cleared,
                    alarm.state.value if isinstance(alarm.state, AlarmState) else str(alarm.state),
                    alarm.value_at_trigger,
                    alarm.acknowledged_by,
                    alarm.acknowledged_at,
                    alarm.cleared_by                )
                records.append(record)
            
            async with self.db_pool.acquire() as conn:
                await conn.executemany(insert_query, records)
            
            logger.info(f"Successfully added {len(validated_alarms)} new alarms to database.")
            
            # Invalidate cache
            await self._invalidate_cache()
            
            return True
            
        except Exception as e:
            logger.error(f"CRITICAL: Failed to add alarms to database: {e}", exc_info=True)
            raise

    async def get_active_alarms(self) -> List[Dict]:
        """Mendapatkan semua alarm yang aktif (belum di-ack/di-clear), dengan caching."""
        cache_key = "alarms:active"
        
        # Coba ambil dari cache dulu
        cached_data = await self._get_from_cache(cache_key)
        if cached_data:
            try:
                alarms_data = json.loads(cached_data)
                logger.debug("Retrieved active alarms from Redis cache.")
                return alarms_data
            except (json.JSONDecodeError, Exception) as e:
                logger.warning(f"Error parsing cached active alarms: {e}. Falling back to database.")

        # Jika tidak ada di cache atau error, ambil dari database
        if not self.db_pool:
            logger.error("Database pool not initialized.")
            return []

        query = """
        SELECT id, rule_id, name, description, tag_id, severity, 
               timestamp_triggered, timestamp_cleared, state, value_at_trigger,
               acknowledged_by, acknowledged_at, cleared_by, cleared_at
        FROM alarms 
        WHERE state = 'active' 
        ORDER BY timestamp_triggered DESC
        """
        
        try:
            async with self.db_pool.acquire() as conn:
                rows = await conn.fetch(query)
            
            alarms = []
            for row in rows:
                alarm_dict = {
                    "id": row['id'],
                    "rule_id": row['rule_id'],
                    "name": row['name'],
                    "description": row['description'],
                    "tag_id": row['tag_id'],
                    "severity": row['severity'],
                    "timestamp_triggered": row['timestamp_triggered'].isoformat() if row['timestamp_triggered'] else None,
                    "timestamp_cleared": row['timestamp_cleared'].isoformat() if row['timestamp_cleared'] else None,
                    "state": row['state'],
                    "value_at_trigger": row['value_at_trigger'],
                    "acknowledged_by": row['acknowledged_by'],
                    "acknowledged_at": row['acknowledged_at'].isoformat() if row['acknowledged_at'] else None,
                    "cleared_by": row['cleared_by'],
                    "cleared_at": row['cleared_at'].isoformat() if row['cleared_at'] else None,
                    "created_at": row['created_at'].isoformat() if row['created_at'] else None,
                    "updated_at": row['updated_at'].isoformat() if row['updated_at'] else None
                }
                alarms.append(alarm_dict)
            
            # Simpan ke cache
            await self._store_in_cache(cache_key, alarms)
            
            return alarms
            
        except Exception as e:
            logger.error(f"Error fetching active alarms from database: {e}")
            return []

    async def acknowledge_alarm(self, alarm_id: str, acknowledged_by: Optional[str] = None) -> bool:
        """Meng-acknowledge sebuah alarm di database dan memperbarui cache."""
        if not self.db_pool:
            logger.error("Database pool not initialized.")
            return False

        acknowledged_at = datetime.now()
        update_query = """
        UPDATE alarms 
        SET state = 'acknowledged', 
            acknowledged_by = $2, 
            acknowledged_at = $3,
            updated_at = NOW()
        WHERE id = $1 AND state = 'active'
        """
        
        try:
            async with self.db_pool.acquire() as conn:
                result = await conn.execute(update_query, alarm_id, acknowledged_by, acknowledged_at)
            
            # result adalah string seperti 'UPDATE 1' atau 'UPDATE 0'
            rows_affected = int(result.split()[-1])
            
            if rows_affected > 0:
                logger.info(f"Alarm {alarm_id} acknowledged in database by {acknowledged_by}.")
                
                # Invalidate cache
                await self._invalidate_cache()
                
                return True
            else:
                logger.warning(f"Alarm {alarm_id} not found or not active for acknowledgement.")
                return False
                
        except Exception as e:
            logger.error(f"Error acknowledging alarm {alarm_id}: {e}")
            return False

    async def clear_alarm(self, alarm_id: str, cleared_by: Optional[str] = None) -> bool:
        """Membersihkan/menyelesaikan sebuah alarm di database dan memperbarui cache."""
        if not self.db_pool:
            logger.error("Database pool not initialized.")
            return False

        # Gunakan timestamp sebenarnya
        cleared_at = datetime.now()
        
        update_query = """
        UPDATE alarms 
        SET state = 'cleared', 
            timestamp_cleared = $2, 
            cleared_by = $3,
            cleared_at = $4,
            updated_at = NOW()
        WHERE id = $1 AND state IN ('active', 'acknowledged')
        """
        
        try:
            async with self.db_pool.acquire() as conn:
                result = await conn.execute(update_query, alarm_id, cleared_at, cleared_by, cleared_at)
            
            rows_affected = int(result.split()[-1])
            
            if rows_affected > 0:
                logger.info(f"Alarm {alarm_id} cleared in database by {cleared_by}.")
                
                # Invalidate cache
                await self._invalidate_cache()
                
                return True
            else:
                logger.warning(f"Alarm {alarm_id} not found or already cleared.")
                return False
                
        except Exception as e:
            logger.error(f"Error clearing alarm {alarm_id}: {e}")
            return False

    async def get_alarm_history(self, limit: int = 100) -> List[Dict]:
        """Mendapatkan riwayat alarm (semua, diurutkan berdasarkan waktu), dengan caching."""
        cache_key = f"alarms:history:limit:{limit}"
        
        # Coba ambil dari cache dulu
        cached_data = await self._get_from_cache(cache_key)
        if cached_data:
            try:
                alarms_data = json.loads(cached_data)
                logger.debug(f"Retrieved alarm history (limit {limit}) from Redis cache.")
                return alarms_data
            except (json.JSONDecodeError, Exception) as e:
                logger.warning(f"Error parsing cached alarm history: {e}. Falling back to database.")

        # Jika tidak ada di cache atau error, ambil dari database
        if not self.db_pool:
            logger.error("Database pool not initialized.")
            return []

        # Urutkan berdasarkan timestamp_triggered DESC (terbaru dulu)
        query = """
        SELECT id, rule_id, name, description, tag_id, severity, 
               timestamp_triggered, timestamp_cleared, state, value_at_trigger,
               acknowledged_by, acknowledged_at, cleared_by, cleared_at
        FROM alarms 
        ORDER BY timestamp_triggered DESC 
        LIMIT $1
        """
        
        try:
            async with self.db_pool.acquire() as conn:
                rows = await conn.fetch(query, limit)
            
            alarms = []
            for row in rows:
                alarm_dict = {
                    "id": row['id'],
                    "rule_id": row['rule_id'],
                    "name": row['name'],
                    "description": row['description'],
                    "tag_id": row['tag_id'],
                    "severity": row['severity'],
                    "timestamp_triggered": row['timestamp_triggered'].isoformat() if row['timestamp_triggered'] else None,
                    "timestamp_cleared": row['timestamp_cleared'].isoformat() if row['timestamp_cleared'] else None,
                    "state": row['state'],
                    "value_at_trigger": row['value_at_trigger'],
                    "acknowledged_by": row['acknowledged_by'],
                    "acknowledged_at": row['acknowledged_at'].isoformat() if row['acknowledged_at'] else None,
                    "cleared_by": row['cleared_by'],
                    "cleared_at": row['cleared_at'].isoformat() if row['cleared_at'] else None,
                    "created_at": row['created_at'].isoformat() if row['created_at'] else None,
                    "updated_at": row['updated_at'].isoformat() if row['updated_at'] else None
                }
                alarms.append(alarm_dict)
            
            # Simpan ke cache
            await self._store_in_cache(cache_key, alarms)
            
            return alarms
            
        except Exception as e:
            logger.error(f"Error fetching alarm history from database: {e}")
            return []

    async def get_alarm_by_id(self, alarm_id: str) -> Optional[Dict]:
        """Mendapatkan alarm berdasarkan ID."""
        if not self.db_pool:
            logger.error("Database pool not initialized.")
            return None

        query = """
        SELECT id, rule_id, name, description, tag_id, severity, 
               timestamp_triggered, timestamp_cleared, state, value_at_trigger,
               acknowledged_by, acknowledged_at, cleared_by, cleared_at
        FROM alarms 
        WHERE id = $1
        """
        
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, alarm_id)
            
            if row:
                alarm_dict = {
                    "id": row['id'],
                    "rule_id": row['rule_id'],
                    "name": row['name'],
                    "description": row['description'],
                    "tag_id": row['tag_id'],
                    "severity": row['severity'],
                    "timestamp_triggered": row['timestamp_triggered'].isoformat() if row['timestamp_triggered'] else None,
                    "timestamp_cleared": row['timestamp_cleared'].isoformat() if row['timestamp_cleared'] else None,
                    "state": row['state'],
                    "value_at_trigger": row['value_at_trigger'],
                    "acknowledged_by": row['acknowledged_by'],
                    "acknowledged_at": row['acknowledged_at'].isoformat() if row['acknowledged_at'] else None,
                    "cleared_by": row['cleared_by'],
                    "cleared_at": row['cleared_at'].isoformat() if row['cleared_at'] else None,
                    "created_at": row['created_at'].isoformat() if row['created_at'] else None,
                    "updated_at": row['updated_at'].isoformat() if row['updated_at'] else None
                }
                return alarm_dict
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error fetching alarm {alarm_id} from database: {e}")
            return None

    async def _invalidate_cache(self):
        """Invalidate cache keys yang relevan."""
        if self.redis_client:
            try:
                self.redis_client.delete("alarms:active")
                self.redis_client.delete("alarms:history")
                # Hapus semua cache history dengan limit berbeda
                keys = self.redis_client.keys("alarms:history:limit:*")
                if keys:
                    self.redis_client.delete(*keys)
                logger.debug("Invalidated Redis cache for alarms.")
            except Exception as e:
                logger.warning(f"Error invalidating Redis cache: {e}")

    async def _get_from_cache(self, key: str) -> Optional[str]:
        """Mendapatkan data dari cache Redis."""
        if self.redis_client:
            try:
                return self.redis_client.get(key)
            except Exception as e:
                logger.warning(f"Error getting from Redis cache (key: {key}): {e}")
        return None

    async def _store_in_cache(self, key: str, data: List[Dict]):
        """Menyimpan data ke cache Redis."""
        if self.redis_client:
            try:
                data_json = json.dumps(data, default=str)
                self.redis_client.setex(key, self.cache_ttl, data_json)
                logger.debug(f"Stored data in Redis cache (key: {key}).")
            except Exception as e:
                logger.warning(f"Error storing in Redis cache (key: {key}): {e}")

    async def close(self):
        """Menutup koneksi database dan Redis."""
        try:
            # Tutup PostgreSQL pool
            if self.db_pool:
                await self.db_pool.close()
                logger.info("PostgreSQL pool for AlarmManager closed.")

            # Tutup Redis client
            if self.redis_client:
                await asyncio.get_event_loop().run_in_executor(
                    None, self.redis_client.close
                )
                logger.info("Redis client for AlarmManager closed.")
                
        except Exception as e:
            logger.error(f"Error closing AlarmManager connections: {e}")