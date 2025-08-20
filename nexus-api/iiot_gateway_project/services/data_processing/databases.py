# services/event_alarm/core/database.py
"""
Konfigurasi database menggunakan SQLAlchemy async.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

# --- Konfigurasi ---
# Menggunakan DATABASE_URL dari config.py Anda
from .config import config # Pastikan config.py meng-export DATABASE_URL

# --- Engine ---
# create_async_engine adalah titik masuk utama untuk koneksi async
engine = create_async_engine(
    config.DATABASE_URL_ASYN,
    # Opsi tambahan bisa ditambahkan di sini
    # echo=True, # Untuk debugging, cetak SQL yang dijalankan
    # pool_size=10,
    # max_overflow=20,
)

# --- Session Factory ---
# async_sessionmaker membuat factory untuk session async
# expire_on_commit=False berarti objek tidak expired setelah commit,
# memungkinkan akses atribut setelah commit dalam scope yang sama.
AsyncSessionFactory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# --- Base Class untuk Model ---
# Semua model Anda akan mewarisi dari Base ini
Base = declarative_base()

# --- Fungsi untuk mendapatkan session (dependency) ---
async def get_db_session() -> AsyncSession:
    """Dependency untuk mendapatkan session database"""
    async with AsyncSessionFactory() as session:
        yield session

# --- Fungsi untuk inisialisasi tabel ---
async def init_db():
    """Membuat semua tabel berdasarkan definisi model."""
    # Import semua model di sini untuk memastikan mereka dikenali oleh Base
    # Misalnya: from ..models.alarm_model import AlarmModel
    # Untuk sekarang, kita impor di dalam fungsi init_db_models
    
    async with engine.begin() as conn:
        # Membuat semua tabel yang didefinisikan dan belum ada
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables initialized.")

# --- Fungsi untuk membersihkan (opsional, saat shutdown) ---
async def close_db():
    """Menutup engine database."""
    await engine.dispose()
    print("Database engine closed.")
