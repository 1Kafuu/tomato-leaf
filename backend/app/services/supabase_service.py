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

    client = create_client(settings.SUPABASE_URL, supabase_key)
    return client

def has_service_role() -> bool:
    """True hanya jika service role key dikonfigurasi (bukan anon key)."""
    return bool(settings.SUPABASE_SERVICE_ROLE_KEY)

async def upload_image_to_storage(file_bytes: bytes, file_name: str) -> str:
    """
    Uploads an image to Supabase Storage and returns the public URL.

    Requirements:
    - Supabase Storage bucket named "images" must exist
    - RLS policy must allow service role or authenticated uploads to "predictions/*" path
    - SUPABASE_SERVICE_ROLE_KEY should be set in .env for server-side uploads

    Returns:
        Public URL string on success, or empty string on failure.
    """
    supabase = get_supabase_client()
    if not supabase:
        print(
            "⚠️  Supabase not configured (SUPABASE_URL/KEY missing). "
            "Image upload skipped."
        )
        return ""

    if not has_service_role():
        print(
            "⚠️  SUPABASE_SERVICE_ROLE_KEY is not set in .env. "
            "Server is using the anon key, which is subject to RLS. "
            "Set SUPABASE_SERVICE_ROLE_KEY to bypass RLS for server-side uploads."
        )

    bucket_name = "images"
    path = f"predictions/{file_name}"

    try:
        supabase.storage.from_(bucket_name).upload(
            path=path,
            file=file_bytes,
            file_options={"content-type": "image/jpeg"},
        )
        url = supabase.storage.from_(bucket_name).get_public_url(path)
        return url
    except Exception as e:
        error_str = str(e)
        print(f"❌ Storage upload failed for '{file_name}': {error_str}")

        # Provide helpful debugging hints
        if "403" in error_str or "Unauthorized" in error_str or "row-level security" in error_str.lower():
            print(
                "   → Supabase Storage rejected the upload (403 / RLS).\n"
                "   → Pastikan SUPABASE_SERVICE_ROLE_KEY di backend/.env sudah diisi\n"
                "     (bukan anon key). Service role bypasses RLS.\n"
                "   → Atau tambahkan policy INSERT di Supabase Storage untuk bucket 'images'."
            )
        elif "404" in error_str or "not found" in error_str.lower():
            print(
                "   → Bucket 'images' belum dibuat di Supabase Storage. "
                "Buat bucket public 'images' di dashboard."
            )
        elif "connection" in error_str.lower():
            print(
                "   → Cek koneksi ke Supabase dan pastikan SUPABASE_URL benar."
            )

        return ""
