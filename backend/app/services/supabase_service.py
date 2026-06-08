import os
from supabase import create_client, Client
from app.core.config import settings

def get_supabase_client() -> Client | None:
    if not settings.SUPABASE_URL:
        return None

    supabase_key = (
        settings.SUPABASE_SERVICE_ROLE_KEY
        or settings.SUPABASE_KEY
    )

    if not supabase_key:
        return None

    return create_client(settings.SUPABASE_URL, supabase_key)

async def upload_image_to_storage(file_bytes: bytes, file_name: str) -> str:
    """
    Uploads an image to Supabase Storage and returns the public URL.
    
    Requirements:
    - Supabase Storage bucket named "images" must exist
    - RLS policy must allow service role or authenticated uploads to "predictions/*" path
    - SUPABASE_SERVICE_ROLE_KEY should be set in .env for server-side uploads
    """
    supabase = get_supabase_client()
    if not supabase:
        # Fallback if supabase is not configured
        return f"http://localhost:8000/placeholder/{file_name}"
        
    bucket_name = "images"
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
        error_str = str(e)
        print(f"❌ Storage upload failed for '{file_name}': {error_str}")
        
        # Provide helpful debugging hints
        if "403" in error_str or "Unauthorized" in error_str:
            print("   → Check Supabase Storage bucket 'images' exists")
            print("   → Check RLS policy allows uploads (see docs/backend_documentation.md)")
            print("   → Ensure SUPABASE_SERVICE_ROLE_KEY is set in .env")
        elif "connection" in error_str.lower():
            print("   → Check network connectivity to Supabase")
            print("   → Check SUPABASE_URL is correct")
        
        return ""
