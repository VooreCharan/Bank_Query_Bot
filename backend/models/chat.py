from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.ai_agent import BankingAIAgent
from services.banking_data_service import BankingDataService
from models.user import db, User, ChatSession
import uuid
import traceback  # Add this

chat_bp = Blueprint('chat', __name__)
ai_agent = BankingAIAgent()
banking_service = BankingDataService()

@chat_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    """Process chat message"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        query = data.get('message')
        session_id = data.get('session_id', str(uuid.uuid4()))
        bank_name = data.get('bank_name')
        language = data.get('language', 'en')
        
        if not query:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get user's selected bank if not provided
        if not bank_name:
            user = User.query.filter_by(public_id=user_id).first()
            bank_name = user.selected_bank if user else None
        
        print(f"Processing query: {query}")  # Debug log
        print(f"User: {user_id}, Bank: {bank_name}")  # Debug log
        
        # Process query with AI agent
        response = ai_agent.process_query(
            user_id=user_id,
            session_id=session_id,
            query=query,
            bank_name=bank_name,
            language=language
        )
        
        print(f"Response generated: {response}")  # Debug log
        
        return jsonify({
            'session_id': session_id,
            'response': response['answer'],
            'sources': response.get('sources', []),
            'language': response.get('language', 'en')
        }), 200
        
    except Exception as e:
        # Print full error traceback
        print("=" * 50)
        print("ERROR IN CHAT ROUTE:")
        print(traceback.format_exc())
        print("=" * 50)
        
        return jsonify({
            'error': str(e),
            'message': 'Failed to process your message. Please try again.'
        }), 500
