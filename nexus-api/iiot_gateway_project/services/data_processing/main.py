# services/event_alarm/main.py
from fastapi import FastAPI
import uvicorn
from .api.v1 import api_router
from .core.db_integrator import DatabaseIntegrator
from .core.alarm_manager import AlarmManager
import logging
from .databases import init_db, close_db

# Setup logging yang lebih baik
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="IIoT Event & Alarm Service")

# Inisialisasi komponen inti
db_integrator = DatabaseIntegrator()
alarm_manager = AlarmManager() # Instance dibuat di sini

@app.on_event("startup")
async def startup_event():
    """Inisialisasi saat aplikasi startup."""
    logger.info("Starting up application...")
    logger.info("Initializing database connections...")
    try:
        await init_db()  # Inisialisasi DB dengan integrator
        await db_integrator.initialize()
        logger.info("Database integrator initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize DatabaseIntegrator: {e}", exc_info=True)
        # Anda bisa memilih untuk menghentikan startup di sini jika DB kritis
        # raise # Uncomment jika ingin aplikasi tidak jalan tanpa DB

    logger.info("Initializing AlarmManager...")
    try:
        await alarm_manager.initialize()
        # Simpan instance yang terinisialisasi (berhasil atau tidak) ke app.state
        # Tapi tambahkan flag untuk menandai status inisialisasi
        app.state.alarm_manager = alarm_manager
        app.state.alarm_manager_initialized = True # Flag baru
        logger.info("AlarmManager initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize AlarmManager: {e}", exc_info=True)
        # Simpan instance yang gagal di-init juga, dan flag-nya False
        app.state.alarm_manager = alarm_manager
        app.state.alarm_manager_initialized = False
        # Anda bisa memilih untuk menghentikan startup jika AlarmManager kritis
        # raise # Uncomment jika ingin aplikasi tidak jalan tanpa AlarmManager

    # Simpan db_integrator juga jika diperlukan di tempat lain
    app.state.db_integrator = db_integrator
    
    logger.info("Startup process completed (with potential errors logged above)")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup saat aplikasi shutdown."""
    await close_db()
    logger.info("Shutting down application...")
    # Tambahkan cleanup jika diperlukan

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "IIoT Event & Alarm Service"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
