import os
from supabase import create_client, Client
from app.core.config import settings

def get_supabase_client() -> Client | None:
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        return None
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

async def upload_image_to_storage(file_bytes: bytes, file_name: str) -> str:
    """
    Uploads an image to Supabase Storage and returns the public URL.
    """
    supabase = get_supabase_client()
    if not supabase:
        # Fallback if supabase is not configured
        return f"http://localhost:8000/placeholder/{file_name}"
        
    bucket_name = "images"
    # Ensure file_name is unique or handled correctly
    path = f"predictions/{file_name}"
    
    try:
        supabase.storage.from_(bucket_name).upload(
            path=path,
            file=file_bytes,
            file_options={"content-type": "image/jpeg"}
        )
        url = supabase.storage.from_(bucket_name).get_public_url(path)
        return url
    except Exception as e:
        print(f"Failed to upload image: {e}")
        return ""
