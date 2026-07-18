from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    preferred_language = db.Column(db.String(10), default='en')
    selected_bank = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'public_id': self.public_id,
            'username': self.username,
            'email': self.email,
            'preferred_language': self.preferred_language,
            'selected_bank': self.selected_bank,
            'created_at': self.created_at.isoformat()
        }

class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(50), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(50), db.ForeignKey('users.public_id'), nullable=False)
    bank_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'session_id': self.session_id,
            'user_id': self.user_id,
            'bank_name': self.bank_name,
            'created_at': self.created_at.isoformat()
        }
