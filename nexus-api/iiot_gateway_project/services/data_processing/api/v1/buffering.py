# api/v1/buffering.py
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List
import logging

# Import dari schemas, bukan models
from ...models.data_processing import BufferedDataEntryResponse
from ...core.buffer_manager import BufferManager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/buffering", tags=["buffering"])

# Dependency untuk mendapatkan BufferManager
async def get_buffer_manager(request: Request) -> BufferManager:
    """
    Dependency untuk mendapatkan instance BufferManager.
    Dalam implementasi produksi, Anda bisa mendapatkan ini dari app state.
    """
    # Untuk sekarang, kita buat instance baru
    # Dalam produksi, sebaiknya gunakan singleton dari app state
    return BufferManager()

@router.get("/status")
async def get_buffer_status(buffer_manager: BufferManager = Depends(get_buffer_manager)):
    """Get current buffering status."""
    try:
        # Implementasi sederhana - bisa diperluas untuk informasi lebih detail
        return {
            "status": "active", 
            "message": "Buffer manager is running. Use specific endpoints for detailed stats."
        }
    except Exception as e:
        logger.error(f"Failed to get buffer status: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve buffer status: {str(e)}")

@router.get("/pending/{destination}", response_model=List[BufferedDataEntryResponse])
async def get_pending_entries(
    destination: str, 
    limit: int = 10,
    buffer_manager: BufferManager = Depends(get_buffer_manager)
):
    """Get pending entries for a destination."""
    try:
        entries_dict = buffer_manager.get_pending_entries(destination, limit)
        
        # Konversi dictionary ke Pydantic model
        entries = []
        for entry_dict in entries_dict:
            try:
                entry = BufferedDataEntryResponse(**entry_dict)
                entries.append(entry)
            except Exception as e:
                logger.warning(f"Failed to convert entry to response model: {e}")
                # Lewati entry yang tidak valid
        
        return entries
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve entries for destination {destination}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve entries: {str(e)}")

@router.get("/size/{destination}")
async def get_buffer_size(
    destination: str,
    buffer_manager: BufferManager = Depends(get_buffer_manager)
):
    """Get the number of pending entries in buffer for a destination."""
    try:
        size = buffer_manager.get_buffer_size(destination)
        return {
            "destination": destination,
            "pending_count": size,
            "status": "empty" if size == 0 else "has_pending_data"
        }
    except Exception as e:
        logger.error(f"Failed to get buffer size for destination {destination}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve buffer size: {str(e)}")

@router.delete("/clear/{destination}")
async def clear_buffer(
    destination: str,
    buffer_manager: BufferManager = Depends(get_buffer_manager)
):
    """Clear all entries from buffer for a destination."""
    try:
        # Cek apakah buffer kosong
        if buffer_manager.is_destination_buffer_empty(destination):
            return {"message": f"Buffer for destination '{destination}' is already empty."}
        
        # Untuk implementasi yang lebih kompleks, Anda mungkin perlu
        # menambahkan method khusus di BufferManager untuk clear buffer
        # Untuk sekarang, kita return pesan informasi
        return {
            "message": f"Buffer clear operation for destination '{destination}' would be implemented here.",
            "note": "In production, this would remove all pending entries for the destination."
        }
        
    except Exception as e:
        logger.error(f"Failed to clear buffer for destination {destination}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to clear buffer: {str(e)}")

@router.post("/acknowledge/{destination}")
async def acknowledge_entries(
    destination: str,
    entry_ids: List[str],
    buffer_manager: BufferManager = Depends(get_buffer_manager)
):
    """Acknowledge and remove specific entries from buffer."""
    try:
        removed_count = buffer_manager.acknowledge_and_remove(destination, entry_ids)
        return {
            "message": f"Successfully acknowledged and removed {removed_count} entries.",
            "destination": destination,
            "requested_count": len(entry_ids),
            "removed_count": removed_count
        }
    except Exception as e:
        logger.error(f"Failed to acknowledge entries for destination {destination}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to acknowledge entries: {str(e)}")