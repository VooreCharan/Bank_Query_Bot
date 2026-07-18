from supabase import create_client, Client
from config import Config
import numpy as np

class VectorDB:
    def __init__(self):
        self.supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        self.collection_name = Config.COLLECTION_NAME
        
    def create_tables(self):
        """Create necessary tables in Supabase"""
        # This SQL should be run in Supabase SQL editor
        sql = """
        -- Enable pgvector extension
        CREATE EXTENSION IF NOT EXISTS vector;
        
        -- Create memory table
        CREATE TABLE IF NOT EXISTS chatbot_memory (
            id BIGSERIAL PRIMARY KEY,
            user_id VARCHAR(255),
            session_id VARCHAR(255),
            question TEXT,
            answer TEXT,
            embedding vector(768),
            metadata JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );
        
        -- Create index for similarity search
        CREATE INDEX IF NOT EXISTS chatbot_memory_embedding_idx 
        ON chatbot_memory USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100);
        
        -- Create banking updates table
        CREATE TABLE IF NOT EXISTS banking_updates (
            id BIGSERIAL PRIMARY KEY,
            title TEXT,
            description TEXT,
            category VARCHAR(100),
            source VARCHAR(255),
            url TEXT,
            bank_name VARCHAR(255),
            created_at TIMESTAMP DEFAULT NOW()
        );
        """
        return sql
    
    def insert_memory(self, user_id, session_id, question, answer, embedding, metadata=None):
        """Insert a memory into the vector database"""
        try:
            data = {
                "user_id": user_id,
                "session_id": session_id,
                "question": question,
                "answer": answer,
                "embedding": embedding.tolist() if isinstance(embedding, np.ndarray) else embedding,
                "metadata": metadata or {}
            }
            
            result = self.supabase.table("chatbot_memory").insert(data).execute()
            return result
        except Exception as e:
            print(f"Error inserting memory: {e}")
            return None
    
    def search_similar_memories(self, query_embedding, user_id=None, limit=5, threshold=0.7):
        """Search for similar memories using vector similarity"""
        try:
            # Convert embedding to list if numpy array
            if isinstance(query_embedding, np.ndarray):
                query_embedding = query_embedding.tolist()
            
            # Build query
            query = self.supabase.rpc(
                'match_chatbot_memory',
                {
                    'query_embedding': query_embedding,
                    'match_threshold': threshold,
                    'match_count': limit,
                    'user_id_filter': user_id
                }
            ).execute()
            
            return query.data if query.data else []
        except Exception as e:
            print(f"Error searching memories: {e}")
            return []
    
    def get_user_memory_summary(self, user_id, limit=20):
        """Get recent memory summary for a user"""
        try:
            result = self.supabase.table("chatbot_memory")\
                .select("*")\
                .eq("user_id", user_id)\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()
            
            return result.data if result.data else []
        except Exception as e:
            print(f"Error getting memory summary: {e}")
            return []

# RPC function SQL (run this in Supabase SQL editor)
"""
CREATE OR REPLACE FUNCTION match_chatbot_memory(
  query_embedding vector(768),
  match_threshold float,
  match_count int,
  user_id_filter text DEFAULT NULL
)
RETURNS TABLE (
  id bigint,
  user_id varchar,
  session_id varchar,
  question text,
  answer text,
  metadata jsonb,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    chatbot_memory.id,
    chatbot_memory.user_id,
    chatbot_memory.session_id,
    chatbot_memory.question,
    chatbot_memory.answer,
    chatbot_memory.metadata,
    1 - (chatbot_memory.embedding <=> query_embedding) AS similarity
  FROM chatbot_memory
  WHERE 
    (user_id_filter IS NULL OR chatbot_memory.user_id = user_id_filter)
    AND 1 - (chatbot_memory.embedding <=> query_embedding) > match_threshold
  ORDER BY chatbot_memory.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
"""
