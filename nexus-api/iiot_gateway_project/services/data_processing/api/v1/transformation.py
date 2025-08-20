# api/v1/transformation.py
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List
from ...models.data_processing import (
    TransformFunctionResponse, 
    ProcessedDataBatchCreate,
    ProcessedDataBatchResponse,
    DataPointResponse
)
from ...core.transformer import DataTransformer
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/transformation", tags=["transformation"])

# Dependency untuk mendapatkan DataTransformer
async def get_data_transformer(request: Request) -> DataTransformer:
    """
    Dependency untuk mendapatkan instance DataTransformer.
    """
    # Dalam implementasi produksi, Anda bisa mendapatkan ini dari app state
    # atau menggunakan dependency injection yang lebih kompleks
    return DataTransformer()

# Placeholder untuk penyimpanan fungsi (di produksi gunakan database)
# Catatan: Dalam produksi, ini akan diambil dari database
def get_transform_functions_store():
    return [
        {
            "id": "1", 
            "name": "Scale 0-100 to 0-1000", 
            "type": "scale", 
            "parameters": {"input_min": 0, "input_max": 100, "output_min": 0, "output_max": 1000},
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    ]

@router.get("/functions", response_model=List[TransformFunctionResponse])
async def list_transform_functions():
    """List available transformation functions."""
    try:
        functions = get_transform_functions_store()
        return [TransformFunctionResponse(**func) for func in functions]
    except Exception as e:
        logger.error(f"Failed to list transform functions: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to list transform functions: {str(e)}")

@router.post("/apply", response_model=ProcessedDataBatchResponse)
async def apply_transformations(
    data_batch: ProcessedDataBatchCreate,
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """
    Apply transformations to a batch of data.
    In a real scenario, you would fetch the transform functions by their IDs.
    """
    try:
        # Misal, client mengirimkan ID fungsi
        # transform_ids = data_batch.metadata.get("transform_ids", [])
        # transforms = [f for f in transform_functions_store if f.id in transform_ids]
        
        # Untuk demo, gunakan fungsi pertama yang ada
        transform_functions_store = get_transform_functions_store()
        transforms = transform_functions_store[:1] if transform_functions_store else []
        
        if not transforms:
            raise HTTPException(status_code=400, detail="No transformations specified or available.")

        # Konversi data points untuk transformer
        # Anda mungkin perlu menyesuaikan ini tergantung pada implementasi DataTransformer
        data_points_dict = [point.dict() for point in data_batch.data_points]
        
        # Terapkan transformasi
        transformed_points_dict = transformer.apply_transformations(data_points_dict, transforms)
        
        # Konversi kembali ke Pydantic models
        transformed_points = [DataPointResponse(**point) for point in transformed_points_dict]
        
        # Buat batch baru untuk hasil
        result_batch_data = {
            "id": str(uuid.uuid4()),
            "batch_id": f"result_{data_batch.batch_id}",
            "data_points_count": len(transformed_points),
            "processed_at": datetime.now(),
            "status": "completed",
            "error_message": None,
            "created_at": datetime.now()
        }
        
        result_batch = ProcessedDataBatchResponse(**result_batch_data)
        return result_batch
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Transformation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Transformation failed: {str(e)}")