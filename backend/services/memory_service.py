from langchain_google_genai import GoogleGenerativeAIEmbeddings
from database.db_setup import VectorDB
from config import Config
import numpy as np

class MemoryService:
    def __init__(self):
        try:
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=Config.GOOGLE_API_KEY
            )
        except Exception as e:
            print(f"Warning: Could not initialize embeddings: {e}")
            self.embeddings = None
        
        self.vector_db = VectorDB()
    
    def create_embedding(self, text):
        """Create embedding for text"""
        if not self.embeddings:
            print("Embeddings not available, skipping...")
            return None
        
        try:
            embedding = self.embeddings.embed_query(text)
            return np.array(embedding)
        except Exception as e:
            print(f"Error creating embedding: {e}")
            return None
    
    def store_conversation(self, user_id, session_id, question, answer, metadata=None):
        """Store conversation in vector database"""
        try:
            # Skip if embeddings not available
            if not self.embeddings:
                print("Skipping memory storage (embeddings unavailable)")
                return False
                
            question_embedding = self.create_embedding(question)
            
            if question_embedding is not None:
                self.vector_db.insert_memory(
                    user_id=user_id,
                    session_id=session_id,
                    question=question,
                    answer=answer,
                    embedding=question_embedding,
                    metadata=metadata
                )
                return True
            return False
        except Exception as e:
            print(f"Error storing conversation: {e}")
            return False
    
    def retrieve_relevant_memories(self, query, user_id=None, limit=5):
        """Retrieve relevant memories based on query"""
        try:
            if not self.embeddings:
                return []
                
            query_embedding = self.create_embedding(query)
            
            if query_embedding is not None:
                memories = self.vector_db.search_similar_memories(
                    query_embedding=query_embedding,
                    user_id=user_id,
                    limit=limit,
                    threshold=0.7
                )
                return memories
            return []
        except Exception as e:
            print(f"Error retrieving memories: {e}")
            return []
    
    def get_conversation_context(self, user_id, limit=10):
        """Get recent conversation context for user"""
        try:
            memories = self.vector_db.get_user_memory_summary(user_id, limit)
            
            context = []
            for memory in memories:
                context.append({
                    'question': memory.get('question'),
                    'answer': memory.get('answer'),
                    'timestamp': memory.get('created_at')
                })
            
            return context
        except Exception as e:
            print(f"Error getting conversation context: {e}")
            return []
