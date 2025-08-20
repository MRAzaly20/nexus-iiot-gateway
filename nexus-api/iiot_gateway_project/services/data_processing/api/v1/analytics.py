# api/v1/analytics.py
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List
import logging
from datetime import datetime
import uuid

# Import dari schemas, bukan models
from ...models.analytics import (
    AnalyticsJobResponse, 
    AnalyticsJobCreate, 
    AnalyticsJobUpdate,
    AnalyticsResultResponse,
    AnalyticsResultCreate,
    DataPointResponse
)
from ...core.analytics_engine import AnalyticsEngine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analytics", tags=["analytics"])

# Dependency untuk mendapatkan AnalyticsEngine
async def get_analytics_engine(request: Request) -> AnalyticsEngine:
    """
    Dependency untuk mendapatkan instance AnalyticsEngine.
    """
    # Dalam implementasi produksi, Anda bisa mendapatkan ini dari app state
    return AnalyticsEngine()

# Placeholder untuk job (dalam produksi, ambil dari database)
def get_analytics_jobs_store():
    return [
        {
            "id": "1", 
            "name": "Temperature Stats", 
            "type": "statistics", 
            "input_tag_ids": ["temp_sensor_01"], 
            "parameters": {}, 
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    ]

@router.get("/configurations", response_model=List[AnalyticsJobResponse])
async def list_analytics_configs():
    """List analytics configurations."""
    try:
        jobs = get_analytics_jobs_store()
        return [AnalyticsJobResponse(**job) for job in jobs]
    except Exception as e:
        logger.error(f"Failed to list analytics configurations: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve analytics configurations: {str(e)}")

@router.get("/configurations/{job_id}", response_model=AnalyticsJobResponse)
async def get_analytics_config(job_id: str):
    """Get a specific analytics configuration by ID."""
    try:
        jobs = get_analytics_jobs_store()
        job = next((j for j in jobs if j["id"] == job_id), None)
        
        if not job:
            raise HTTPException(status_code=404, detail="Analytics job not found")
            
        return AnalyticsJobResponse(**job)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get analytics configuration {job_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve analytics configuration: {str(e)}")

@router.post("/configurations", response_model=AnalyticsJobResponse, status_code=201)
async def create_analytics_config(job: AnalyticsJobCreate):
    """Create a new analytics configuration."""
    try:
        # Dalam produksi, simpan ke database
        new_job = {
            "id": str(uuid.uuid4()),
            "name": job.name,
            "type": job.type,
            "input_tag_ids": job.input_tag_ids or [],
            "parameters": job.parameters or {},
            "is_active": job.is_active,
            "schedule": job.schedule,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # Simulasi penyimpanan
        logger.info(f"Created new analytics job: {job.name}")
        
        return AnalyticsJobResponse(**new_job)
    except Exception as e:
        logger.error(f"Failed to create analytics configuration: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to create analytics configuration: {str(e)}")

@router.put("/configurations/{job_id}", response_model=AnalyticsJobResponse)
async def update_analytics_config(job_id: str, job: AnalyticsJobUpdate):
    """Update an existing analytics configuration."""
    try:
        jobs = get_analytics_jobs_store()
        existing_job = next((j for j in jobs if j["id"] == job_id), None)
        
        if not existing_job:
            raise HTTPException(status_code=404, detail="Analytics job not found")

        # Update fields yang disediakan
        updated_job = existing_job.copy()
        update_data = job.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            if value is not None:
                updated_job[field] = value
                
        updated_job["updated_at"] = datetime.now()
        
        # Simulasi update
        logger.info(f"Updated analytics job: {job_id}")
        
        return AnalyticsJobResponse(**updated_job)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update analytics configuration {job_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to update analytics configuration: {str(e)}")

@router.delete("/configurations/{job_id}")
async def delete_analytics_config(job_id: str):
    """Delete an analytics configuration."""
    try:
        jobs = get_analytics_jobs_store()
        job_exists = any(j["id"] == job_id for j in jobs)
        
        if not job_exists:
            raise HTTPException(status_code=404, detail="Analytics job not found")
            
        # Simulasi penghapusan
        logger.info(f"Deleted analytics job: {job_id}")
        
        return {
            "message": f"Analytics job {job_id} deleted successfully",
            "job_id": job_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete analytics configuration {job_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to delete analytics configuration: {str(e)}")

@router.post("/run", response_model=AnalyticsResultResponse)
async def run_analytics_job(
    job_id: str, 
    data: List[DataPointResponse],
    analytics_engine: AnalyticsEngine = Depends(get_analytics_engine)
):
    """Run an analytics job on provided data."""
    try:
        jobs = get_analytics_jobs_store()
        job_dict = next((j for j in jobs if j["id"] == job_id), None)
        
        if not job_dict:
            raise HTTPException(status_code=404, detail="Analytics job not found")
            
        if not job_dict["is_active"]:
            raise HTTPException(status_code=400, detail="Analytics job is not active")

        # Konversi job ke Pydantic model
        job = AnalyticsJobResponse(**job_dict)
        
        # Konversi data points ke format yang dibutuhkan
        data_points_dict = [point.dict() for point in data]
        
        # Jalankan job analytics
        # result = analytics_engine.run_job(job, data_points_dict)
        
        # Untuk contoh, kita buat result dummy
        result_data = {
            "id": str(uuid.uuid4()),
            "job_id": job_id,
            "timestamp": datetime.now(),
            "result_data": {
                "message": f"Analytics job {job.name} would run here with {len(data)} data points",
                "sample_result": "processed_data"
            },
            "execution_time_ms": 150,
            "status": "success",
            "created_at": datetime.now()
        }
        
        return AnalyticsResultResponse(**result_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analytics job {job_id} failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analytics job failed: {str(e)}")

@router.get("/results/{job_id}", response_model=List[AnalyticsResultResponse])
async def get_analytics_results(job_id: str, limit: int = 10):
    """Get results for a specific analytics job."""
    try:
        # Dalam produksi, ambil dari database
        # Untuk contoh, kita buat hasil dummy
        dummy_results = []
        for i in range(min(limit, 3)):
            result_data = {
                "id": str(uuid.uuid4()),
                "job_id": job_id,
                "timestamp": datetime.now(),
                "result_data": {
                    "result_number": i + 1,
                    "data": f"Sample result {i + 1}"
                },
                "execution_time_ms": 100 + i * 50,
                "status": "success",
                "created_at": datetime.now()
            }
            dummy_results.append(AnalyticsResultResponse(**result_data))
            
        return dummy_results
        
    except Exception as e:
        logger.error(f"Failed to get analytics results for job {job_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve analytics results: {str(e)}")

@router.post("/configurations/{job_id}/toggle", response_model=AnalyticsJobResponse)
async def toggle_analytics_job(job_id: str):
    """Toggle the active status of an analytics job."""
    try:
        jobs = get_analytics_jobs_store()
        existing_job = next((j for j in jobs if j["id"] == job_id), None)
        
        if not existing_job:
            raise HTTPException(status_code=404, detail="Analytics job not found")

        # Toggle is_active status
        existing_job["is_active"] = not existing_job["is_active"]
        existing_job["updated_at"] = datetime.now()
        
        # Simulasi update
        status = "activated" if existing_job["is_active"] else "deactivated"
        logger.info(f"Analytics job {job_id} {status}")
        
        return AnalyticsJobResponse(**existing_job)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to toggle analytics job {job_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to toggle analytics job: {str(e)}")