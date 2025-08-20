# api/v1/storage.py
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List
import logging
from datetime import datetime

# Import dari schemas, bukan models
from ...models.data_processing import (
    StorageConfigResponse, 
    StorageConfigCreate,
    StorageConfigUpdate,
    DataPointResponse
)
from ...core.db_integrator import DatabaseIntegrator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/storage", tags=["storage"])

# Placeholder untuk konfigurasi storage (dalam produksi, ambil dari database)
def get_storage_configs_store():
    return [
        {
            "id": "1", 
            "name": "Local InfluxDB", 
            "type": "influxdb", 
            "connection_string": "url=http://localhost:8086;token=my-token;org=my-org;bucket=my-bucket", 
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "id": "2", 
            "name": "Cloud Timescale", 
            "type": "postgres", 
            "connection_string": "postgresql://...", 
            "is_active": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    ]

# Dependency untuk mendapatkan DatabaseIntegrator
async def get_db_integrator(request: Request) -> DatabaseIntegrator:
    """
    Dependency untuk mendapatkan instance DatabaseIntegrator yang sudah diinisialisasi.
    """
    # Dalam implementasi produksi, Anda bisa mendapatkan ini dari app state
    return DatabaseIntegrator()

@router.get("/configurations", response_model=List[StorageConfigResponse])
async def list_storage_configs():
    """List storage configurations."""
    try:
        configs = get_storage_configs_store()
        return [StorageConfigResponse(**config) for config in configs]
    except Exception as e:
        logger.error(f"Failed to list storage configurations: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve storage configurations: {str(e)}")

@router.get("/configurations/{config_id}", response_model=StorageConfigResponse)
async def get_storage_config(config_id: str):
    """Get a specific storage configuration by ID."""
    try:
        configs = get_storage_configs_store()
        config = next((c for c in configs if c["id"] == config_id), None)
        
        if not config:
            raise HTTPException(status_code=404, detail="Storage configuration not found")
            
        return StorageConfigResponse(**config)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get storage configuration {config_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve storage configuration: {str(e)}")

@router.post("/test")
async def test_storage_connection(config: StorageConfigCreate):
    """Test connection to a storage backend."""
    try:
        # Ini akan memerlukan inisialisasi db_integrator yang benar
        # dan mungkin membuat koneksi sementara.
        # Untuk contoh, kita kembalikan response yang lebih informatif.
        return {
            "message": f"Test connection logic for {config.type} would go here.",
            "config_name": config.name,
            "config_type": config.type,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to test storage connection: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to test storage connection: {str(e)}")

@router.post("/write")
async def write_data_to_storage(
    data_batch: List[DataPointResponse], 
    config_id: str, 
    db: DatabaseIntegrator = Depends(get_db_integrator)
):
    """Write data to a specific storage backend."""
    try:
        # Dapatkan konfigurasi storage
        configs = get_storage_configs_store()
        config = next((c for c in configs if c["id"] == config_id), None)
        
        if not config:
            raise HTTPException(status_code=404, detail="Storage configuration not found")
            
        if not config["is_active"]:
            raise HTTPException(status_code=400, detail="Storage configuration is not active")

        # Konversi data points ke format yang dibutuhkan
        data_points_dict = [point.dict() for point in data_batch]
        
        # Di implementasi sebenarnya, Anda akan memanggil method write_data
        # await db.write_data(data_points_dict, config)
        
        return {
            "message": f"Successfully processed {len(data_batch)} data points",
            "storage_type": config["type"],
            "storage_name": config["name"],
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to write data to storage {config_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to write data: {str(e)}")

@router.post("/configurations", response_model=StorageConfigResponse, status_code=201)
async def create_storage_config(config: StorageConfigCreate):
    """Create a new storage configuration."""
    try:
        # Dalam produksi, ini akan disimpan ke database
        new_config = {
            "id": "new_id",  # Dalam produksi, generate UUID yang sesungguhnya
            "name": config.name,
            "type": config.type,
            "connection_string": config.connection_string,
            "is_active": config.is_active,
            "config_data": config.config_data,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # Simulasi penyimpanan
        logger.info(f"Created new storage configuration: {config.name}")
        
        return StorageConfigResponse(**new_config)
        
    except Exception as e:
        logger.error(f"Failed to create storage configuration: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to create storage configuration: {str(e)}")

@router.put("/configurations/{config_id}", response_model=StorageConfigResponse)
async def update_storage_config(config_id: str, config: StorageConfigUpdate):
    """Update an existing storage configuration."""
    try:
        configs = get_storage_configs_store()
        existing_config = next((c for c in configs if c["id"] == config_id), None)
        
        if not existing_config:
            raise HTTPException(status_code=404, detail="Storage configuration not found")

        # Update fields yang disediakan
        updated_config = existing_config.copy()
        update_data = config.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            if value is not None:
                updated_config[field] = value
                
        updated_config["updated_at"] = datetime.now()
        
        # Simulasi update
        logger.info(f"Updated storage configuration: {config_id}")
        
        return StorageConfigResponse(**updated_config)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update storage configuration {config_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to update storage configuration: {str(e)}")

@router.delete("/configurations/{config_id}")
async def delete_storage_config(config_id: str):
    """Delete a storage configuration."""
    try:
        configs = get_storage_configs_store()
        config_exists = any(c["id"] == config_id for c in configs)
        
        if not config_exists:
            raise HTTPException(status_code=404, detail="Storage configuration not found")
            
        # Simulasi penghapusan
        logger.info(f"Deleted storage configuration: {config_id}")
        
        return {
            "message": f"Storage configuration {config_id} deleted successfully",
            "config_id": config_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete storage configuration {config_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to delete storage configuration: {str(e)}")