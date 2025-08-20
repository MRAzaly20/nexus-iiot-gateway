# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# Membuat instance aplikasi FastAPI
app = FastAPI(title="API Sederhana", description="Contoh REST API dengan FastAPI")

# --- Model Data (Pydantic) ---
# Ini mendefinisikan struktur data untuk item kita.
class Item(BaseModel):
    id: Optional[int] = None # ID akan diatur oleh server
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

# --- Penyimpanan Data Sementara (Simulasi Database) ---
# Untuk contoh sederhana, kita gunakan list di memori.
# Di produksi, Anda akan menggunakan database sebenarnya (seperti PostgreSQL, MySQL).
items_db = [
    {"id": 1, "name": "Laptop", "description": "Laptop gaming", "price": 12000000.0, "is_available": True},
    {"id": 2, "name": "Mouse", "description": "Mouse wireless", "price": 150000.0, "is_available": True},
]
# Counter sederhana untuk ID
next_id = 3

# --- Operasi CRUD ---

# 1. READ - Dapatkan semua item
#   - Metode HTTP: GET
#   - Path: /items/
#   - Response: List[Item]
@app.get("/items/", response_model=List[Item])
async def read_items():
    """
    Mendapatkan daftar semua item.
    """
    return items_db

# 2. READ - Dapatkan item berdasarkan ID
#   - Metode HTTP: GET
#   - Path: /items/{item_id}
#   - Response: Item
#   - Error Handling: Mengembalikan 404 jika tidak ditemukan
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    """
    Mendapatkan item berdasarkan ID-nya.
    """
    for item in items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# 3. CREATE - Buat item baru
#   - Metode HTTP: POST
#   - Path: /items/
#   - Request Body: Item (tanpa ID)
#   - Response: Item (dengan ID yang dihasilkan)
@app.post("/items/", response_model=Item, status_code=201)
async def create_item(item: Item):
    """
    Membuat item baru.
    """
    global next_id
    # Buat item baru dengan ID yang di-generate
    new_item = item.dict() # Ubah dari Pydantic model ke dictionary
    new_item["id"] = next_id
    items_db.append(new_item)
    next_id += 1
    return new_item # Kembalikan item yang telah dibuat

# 4. UPDATE - Perbarui item berdasarkan ID
#   - Metode HTTP: PUT
#   - Path: /items/{item_id}
#   - Request Body: Item (dengan data yang diperbarui)
#   - Response: Item (yang telah diperbarui)
#   - Error Handling: Mengembalikan 404 jika tidak ditemukan
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item_update: Item):
    """
    Memperbarui item berdasarkan ID-nya.
    """
    for index, item in enumerate(items_db):
        if item["id"] == item_id:
            # Update item di list
            updated_item = item_update.dict()
            updated_item["id"] = item_id # Pastikan ID tetap sama
            items_db[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

# 5. DELETE - Hapus item berdasarkan ID
#   - Metode HTTP: DELETE
#   - Path: /items/{item_id}
#   - Response: dict (konfirmasi penghapusan)
#   - Error Handling: Mengembalikan 404 jika tidak ditemukan
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """
    Menghapus item berdasarkan ID-nya.
    """
    for index, item in enumerate(items_db):
        if item["id"] == item_id:
            items_db.pop(index)
            return {"message": f"Item with id {item_id} has been deleted"}
    raise HTTPException(status_code=404, detail="Item not found")

# --- Endpoint Tambahan: Health Check ---
@app.get("/")
async def root():
    """
    Endpoint dasar untuk memeriksa apakah API berjalan.
    """
    return {"message": "Welcome to the Simple FastAPI REST API!"}

# --- Menjalankan Server (Opsional dalam file ini) ---
# Ini memungkinkan Anda menjalankan file ini langsung dengan `python main.py`
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
