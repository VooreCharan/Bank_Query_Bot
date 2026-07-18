import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///banking_chatbot.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours
    
    # Supabase
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    # Google Gemini
    
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # APIs
    SERPER_API_KEY = os.getenv('SERPER_API_KEY')
    JINA_API_KEY = os.getenv('JINA_API_KEY')
    
    # Vector DB
    EMBEDDING_DIMENSION = 768
    COLLECTION_NAME = "banking_chatbot_memory"
