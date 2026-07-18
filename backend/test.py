from supabase import create_client
from config import Config

print("SUPABASE_URL:", Config.SUPABASE_URL)
print("SUPABASE_KEY starts with:", Config.SUPABASE_KEY[:10] if Config.SUPABASE_KEY else None)
print("SUPABASE_KEY length:", len(Config.SUPABASE_KEY) if Config.SUPABASE_KEY else None)

supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
print("✓ Supabase client created successfully")
