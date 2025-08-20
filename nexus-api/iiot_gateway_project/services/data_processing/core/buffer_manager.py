# core/buffer_manager.py
import redis
import json
import logging
import uuid
from typing import List, Optional
from datetime import datetime
import asyncio

# Import dari schemas, bukan models
from ..models.data_processing import BufferedDataEntryResponse, BufferedDataEntryCreate
from ..config import config
logger = logging.getLogger(__name__)

class BufferManager:
    """
    Mengelola buffering data menggunakan Redis.
    Implementasi Store-and-Forward.
    """
    BUFFER_KEY_PREFIX = "buffer_queue:"

    def __init__(self):
        try:
            self.redis_client = redis.Redis(
                host=config.REDIS_HOST, 
                port=config.REDIS_PORT, 
                db=config.REDIS_DB_BUFFER, 
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True
            )
            # Test koneksi
            self.redis_client.ping()
            logger.info("BufferManager initialized with Redis successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Redis connection: {e}")
            raise

    def enqueue_data(self, destination: str, payload: str) -> str:
        """
        Memasukkan data ke dalam buffer (queue Redis).
        """
        try:
            entry_id = str(uuid.uuid4())
            current_timestamp = datetime.now().isoformat()
            
            # Buat data entry sebagai dictionary
            entry_data = {
                "id": entry_id,
                "destination": destination,
                "payload": payload,
                "timestamp_queued": current_timestamp,
                "retry_count": 0,
                "max_retries": 3,
                "status": "pending",
                "created_at": current_timestamp,
                "updated_at": current_timestamp
            }
            
            key = f"{self.BUFFER_KEY_PREFIX}{destination}"
            serialized_entry = json.dumps(entry_data)
            
            # LPUSH untuk menambahkan ke head queue (FIFO)
            self.redis_client.lpush(key, serialized_entry)
            logger.info(f"Enqueued data (ID: {entry_id}) for destination: {destination}")
            return entry_id
            
        except Exception as e:
            logger.error(f"Failed to enqueue data for destination {destination}: {e}")
            raise

    def get_pending_entries(self, destination: str, limit: int = 10) -> List[dict]:
        """
        Mengambil entry dari buffer untuk sebuah tujuan, tanpa menghapusnya.
        Mengembalikan list of dictionaries untuk kompatibilitas dengan FastAPI.
        """
        try:
            key = f"{self.BUFFER_KEY_PREFIX}{destination}"
            # LRANGE untuk mendapatkan elemen dari list
            entries_raw = self.redis_client.lrange(key, 0, limit - 1)
            
            entries = []
            for entry_str in entries_raw:
                try:
                    entry_dict = json.loads(entry_str)
                    # Validasi dengan Pydantic model (opsional)
                    # BufferedDataEntryResponse(**entry_dict)  # Untuk validasi
                    entries.append(entry_dict)
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to decode entry: {e}")
                    continue
                except Exception as e:
                    logger.warning(f"Failed to validate entry: {e}")
                    continue
                    
            logger.debug(f"Retrieved {len(entries)} pending entries for {destination}.")
            return entries
            
        except Exception as e:
            logger.error(f"Failed to get pending entries for destination {destination}: {e}")
            return []

    def acknowledge_and_remove(self, destination: str, entry_ids: List[str]) -> int:
        """
        Menghapus entry yang telah berhasil dikirim dari buffer.
        Karena Redis List tidak mendukung penghapusan elemen tengah secara efisien,
        kita perlu pendekatan khusus. Untuk kesederhanaan, kita asumsikan
        entry diproses dari yang tertua (head) dan dihapus secara batch.
        """
        try:
            # Pendekatan sederhana: hapus N entry teratas jika entry_ids adalah N entry teratas.
            # Ini bekerja jika konsumen memproses dalam urutan FIFO.
            key = f"{self.BUFFER_KEY_PREFIX}{destination}"
            
            # Dapatkan semua entry untuk memastikan kita hanya menghapus yang benar
            all_entries = self.redis_client.lrange(key, 0, -1)
            if not all_entries:
                return 0
                
            # Hitung berapa banyak entry yang harus dihapus (berdasarkan entry_ids yang diberikan)
            # Asumsikan entry_ids adalah entry teratas yang akan dihapus
            num_to_remove = min(len(entry_ids), len(all_entries))
            
            # Hapus entry teratas
            removed_count = 0
            for _ in range(num_to_remove):
                result = self.redis_client.rpop(key)  # Hapus dari tail (FIFO)
                if result:
                    removed_count += 1
                else:
                    break
                    
            logger.info(f"Acknowledged and removed {removed_count} entries for {destination}.")
            return removed_count
            
        except Exception as e:
            logger.error(f"Failed to acknowledge and remove entries for destination {destination}: {e}")
            return 0

    def increment_retry_count(self, destination: str, entry_id: str) -> bool:
        """
        Meningkatkan jumlah retry untuk sebuah entry.
        Karena keterbatasan LPUSH/LTRIM, ini kompleks.
        Sebagai alternatif, bisa menyimpan retry count di hash terpisah.
        """
        try:
            key = f"{self.BUFFER_KEY_PREFIX}{destination}"
            
            # Dapatkan semua entry
            all_entries = self.redis_client.lrange(key, 0, -1)
            if not all_entries:
                return False
                
            updated_entries = []
            entry_found = False
            
            # Cari dan update entry yang sesuai
            for entry_str in all_entries:
                try:
                    entry_dict = json.loads(entry_str)
                    if entry_dict.get('id') == entry_id:
                        entry_dict['retry_count'] = entry_dict.get('retry_count', 0) + 1
                        entry_dict['updated_at'] = datetime.now().isoformat()
                        entry_found = True
                    updated_entries.append(json.dumps(entry_dict))
                except json.JSONDecodeError:
                    updated_entries.append(entry_str)  # Pertahankan entry yang tidak valid
            
            if entry_found:
                # Hapus semua entry dan tambahkan yang sudah diupdate
                self.redis_client.delete(key)
                if updated_entries:
                    self.redis_client.lpush(key, *updated_entries)
                logger.info(f"Incremented retry count for entry {entry_id}")
                return True
            else:
                logger.warning(f"Entry {entry_id} not found for retry increment")
                return False
                
        except Exception as e:
            logger.error(f"Failed to increment retry count for entry {entry_id}: {e}")
            return False

    def update_entry_status(self, destination: str, entry_id: str, status: str, error_message: Optional[str] = None) -> bool:
        """
        Update status entry dalam buffer.
        """
        try:
            key = f"{self.BUFFER_KEY_PREFIX}{destination}"
            
            # Dapatkan semua entry
            all_entries = self.redis_client.lrange(key, 0, -1)
            if not all_entries:
                return False
                
            updated_entries = []
            entry_found = False
            
            # Cari dan update entry yang sesuai
            for entry_str in all_entries:
                try:
                    entry_dict = json.loads(entry_str)
                    if entry_dict.get('id') == entry_id:
                        entry_dict['status'] = status
                        entry_dict['updated_at'] = datetime.now().isoformat()
                        if error_message:
                            entry_dict['error_message'] = error_message
                        if status == 'completed':
                            entry_dict['completed_at'] = datetime.now().isoformat()
                        entry_found = True
                    updated_entries.append(json.dumps(entry_dict))
                except json.JSONDecodeError:
                    updated_entries.append(entry_str)
            
            if entry_found:
                # Hapus semua entry dan tambahkan yang sudah diupdate
                self.redis_client.delete(key)
                if updated_entries:
                    self.redis_client.lpush(key, *updated_entries)
                logger.info(f"Updated status for entry {entry_id} to {status}")
                return True
            else:
                logger.warning(f"Entry {entry_id} not found for status update")
                return False
                
        except Exception as e:
            logger.error(f"Failed to update entry status for {entry_id}: {e}")
            return False

    def is_destination_buffer_empty(self, destination: str) -> bool:
        """Memeriksa apakah buffer untuk tujuan tertentu kosong."""
        try:
            key = f"{self.BUFFER_KEY_PREFIX}{destination}"
            length = self.redis_client.llen(key)
            return length == 0
        except Exception as e:
            logger.error(f"Failed to check buffer empty status for destination {destination}: {e}")
            return True

    def get_buffer_size(self, destination: str) -> int:
        """Mendapatkan jumlah entry dalam buffer untuk tujuan tertentu."""
        try:
            key = f"{self.BUFFER_KEY_PREFIX}{destination}"
            return self.redis_client.llen(key)
        except Exception as e:
            logger.error(f"Failed to get buffer size for destination {destination}: {e}")
            return 0

    async def close(self):
        """Menutup koneksi Redis."""
        try:
            if hasattr(self, 'redis_client'):
                await asyncio.get_event_loop().run_in_executor(
                    None, self.redis_client.close
                )
            logger.info("BufferManager Redis connection closed.")
        except Exception as e:
            logger.error(f"Error closing Redis connection: {e}")