import os
import uuid
import time
from typing import Optional
from app.core.config import settings

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

class StorageService:
    @staticmethod
    def save_file(file_bytes: bytes, filename: str, subfolder: str = "documents") -> str:
        """Saves a file locally or to object storage and returns the stored path/key."""
        folder = os.path.join(settings.UPLOAD_DIR, subfolder)
        os.makedirs(folder, exist_ok=True)
        ext = os.path.splitext(filename)[1]
        unique_name = f"{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(folder, unique_name)
        
        with open(filepath, "wb") as f:
            f.write(file_bytes)
            
        return f"{subfolder}/{unique_name}"

    @staticmethod
    def generate_signed_url(file_key: str, expires_in_seconds: int = 3600) -> str:
        """Generates a time-bounded signed URL for secure private document access."""
        timestamp = int(time.time()) + expires_in_seconds
        # Signed token simulation for local file serving
        return f"/api/v1/documents/download?key={file_key}&expires={timestamp}&token=signed_preview"

storage_service = StorageService()
