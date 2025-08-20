"""
API Routes untuk mengelola Alarm.
Menyediakan endpoint untuk melihat, mengakui (acknowledge), membersihkan (clear),
mendapatkan riwayat alarm, dan menambahkan alarm baru secara manual.
"""
from fastapi import APIRouter, HTTPException, Depends, Request, status
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid
import logging
import json

# Import model dari schemas (bukan dari models SQLAlchemy)
from ...models.event_alarm import (
    AlarmResponse, 
    AlarmCreateRequest, 
    AlarmState, 
    AlarmSeverity
)
from ...core.alarm_manager import AlarmManager

# Setup logging
logger = logging.getLogger(__name__)

# Membuat router FastAPI dengan prefix dan tag
router = APIRouter(prefix="/alarms", tags=["alarms"])

# --- Dependency untuk mendapatkan AlarmManager ---
async def get_alarm_manager(request: Request) -> AlarmManager:
    """
    Dependency untuk mendapatkan instance AlarmManager yang sudah diinisialisasi.
    """
    if not hasattr(request.app.state, 'alarm_manager'):
        raise HTTPException(status_code=500, detail="AlarmManager setup error: Instance not found.")

    if not getattr(request.app.state, 'alarm_manager_initialized', False):
         raise HTTPException(status_code=500, detail="AlarmManager not initialized. Check server logs for startup errors.")

    return request.app.state.alarm_manager

# --- Endpoint API ---

@router.post("/", response_model=AlarmResponse, status_code=status.HTTP_201_CREATED, summary="Create New Alarm")
async def add_alarm(
    alarm_data: AlarmCreateRequest,
    alarm_manager: AlarmManager = Depends(get_alarm_manager)
):
    """
    Membuat dan menambahkan alarm baru secara manual.
    """
    alarm_dict = alarm_data.model_dump()
    # Convert dictionary to JSON string
    alarm_json = json.dumps(alarm_dict, default=str)
    print(f"Received alarm data: {alarm_dict}")

    try:
        new_alarm_id = str(uuid.uuid4())
        
        # Penanganan timestamp
        if alarm_data.timestamp_triggered:
            triggered_timestamp = alarm_data.timestamp_triggered
        else:
            triggered_timestamp = datetime.now()
        
        # Pembuatan data alarm untuk disimpan
        alarm_dict_data = {
            "id": new_alarm_id,
            "rule_id": alarm_dict['rule_id'],
            "name": alarm_dict['name'],
            "description": alarm_dict['description'],
            "tag_id": alarm_dict['tag_id'],
            "severity": alarm_dict['severity'],
            "timestamp_triggered": triggered_timestamp,
            "timestamp_cleared": None,
            "state": alarm_dict['state'],
            "value_at_trigger": alarm_dict['value_at_trigger']
        }
        
        # Kirim ke AlarmManager untuk disimpan (dalam format dictionary/JSON)
        await alarm_manager._create_tables_if_not_exist()
        await alarm_manager.add_alarms([alarm_dict_data])
        
        # Kembalikan response dalam format Pydantic model
        return AlarmResponse(**alarm_dict_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create alarm: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to create alarm: {str(e)}")

@router.get("/", response_model=List[AlarmResponse], summary="List Alarms")
async def list_current_alarms(
    state: Optional[AlarmState] = None,
    limit: int = 100,
    alarm_manager: AlarmManager = Depends(get_alarm_manager)
):
    """
    Mendapatkan daftar alarm saat ini.

    - **state** (query param, optional): Filter alarm berdasarkan state-nya (active, acknowledged, cleared).
                                     Jika tidak diberikan, secara default hanya mengembalikan alarm 'active'.
    - **limit** (query param, optional): Batasi jumlah alarm yang dikembalikan (default 100, maks 1000).
    """
    try:
        effective_limit = min(limit, 1000)
        
        if state:
            all_alarms = await alarm_manager.get_alarm_history(effective_limit * 2)
            # Konversi ke Pydantic model
            alarm_responses = [AlarmResponse(**alarm.model_dump()) for alarm in all_alarms]
            filtered_alarms = [a for a in alarm_responses if a.state == state]
            return filtered_alarms[:effective_limit]
        else:
            active_alarms = await alarm_manager.get_active_alarms()
            # Konversi ke Pydantic model
            return [AlarmResponse(**alarm.model_dump()) for alarm in active_alarms]
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch alarms: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to fetch alarms: {str(e)}")

@router.put("/{alarm_id}/acknowledge", summary="Acknowledge Alarm")
async def acknowledge_alarm(
    alarm_id: str,
    alarm_manager: AlarmManager = Depends(get_alarm_manager)
):
    """
    Mengakui (acknowledge) sebuah alarm.

    - **alarm_id** (path param): ID unik dari alarm yang ingin di-acknowledge.
    """
    try:
        success = await alarm_manager.acknowledge_alarm(alarm_id)
        
        if not success:
            raise HTTPException(
                status_code=404, 
                detail="Alarm not found, not active, or already acknowledged/cleared."
            )
            
        return {"message": f"Alarm {alarm_id} acknowledged successfully."}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to acknowledge alarm {alarm_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to acknowledge alarm: {str(e)}")

@router.put("/{alarm_id}/clear", summary="Clear Alarm")
async def clear_alarm(
    alarm_id: str,
    alarm_manager: AlarmManager = Depends(get_alarm_manager)
):
    """
    Membersihkan (clear) sebuah alarm.

    - **alarm_id** (path param): ID unik dari alarm yang ingin di-clear.
    """
    try:
        success = await alarm_manager.clear_alarm(alarm_id)
        
        if not success:
            raise HTTPException(
                status_code=404, 
                detail="Alarm not found, already cleared, or in an unexpected state."
            )
            
        return {"message": f"Alarm {alarm_id} cleared successfully."}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to clear alarm {alarm_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to clear alarm: {str(e)}")

@router.get("/history", response_model=List[AlarmResponse], summary="Get Alarm History")
async def get_alarm_history(
    limit: int = 100,
    alarm_manager: AlarmManager = Depends(get_alarm_manager)
):
    """
    Mendapatkan riwayat alarm.

    - **limit** (query param, optional): Batasi jumlah alarm yang dikembalikan (default 100, maks 1000).
    """
    try:
        effective_limit = min(limit, 1000)
        alarms = await alarm_manager.get_alarm_history(effective_limit)
        # Konversi ke Pydantic model
        return [AlarmResponse(**alarm.model_dump()) for alarm in alarms]
        
    except Exception as e:
        logger.error(f"Failed to fetch alarm history: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to fetch alarm history: {str(e)}")