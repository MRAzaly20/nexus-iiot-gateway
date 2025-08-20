# test_db_connection.py
import asyncio
import asyncpg
import os

# --- Konfigurasi (sama seperti di config.py) ---
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Administrator1234")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "iiot_data")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
# Catatan: asyncpg.create_pool() dan connect() menggunakan 'postgresql://' bukan 'postgresql+asyncpg://'

async def test_connection():
    """Fungsi async untuk menguji koneksi."""
    conn = None
    try:
        # Mencoba membuat koneksi tunggal
        print(f"Mencoba menghubungkan ke: {DATABASE_URL}")
        conn = await asyncpg.connect(DATABASE_URL)
        print("✅ Koneksi berhasil!")
        
        # (Opsional) Jalankan query sederhana
        version = await conn.fetchval('SELECT version();')
        print(f"PostgreSQL version: {version}")
        
        # (Opsional) Cek database saat ini
        current_db = await conn.fetchval('SELECT current_database();')
        print(f"Connected to database: {current_db}")

    except asyncpg.exceptions.InvalidPasswordError:
        print("❌ ERROR: Password tidak valid.")
    except asyncpg.exceptions.InvalidAuthorizationSpecificationError:
        print("❌ ERROR: User/Password tidak valid.")
    except asyncpg.exceptions.UndefinedTableError:
        print("❌ ERROR: Database tidak ditemukan.")
    except ConnectionRefusedError:
        print("❌ ERROR: Koneksi ditolak. Pastikan PostgreSQL server berjalan dan port benar.")
    except Exception as e:
        print(f"❌ ERROR tidak terduga: {e}")
    finally:
        if conn:
            await conn.close()
            print("Koneksi ditutup.")

# Menjalankan fungsi async
if __name__ == "__main__":
    asyncio.run(test_connection())
