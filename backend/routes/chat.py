from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.ai_agent import BankingAIAgent
from services.banking_data_service import BankingDataService
from models.user import db, User, ChatSession
import uuid

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
        
        # Process query with AI agent
        response = ai_agent.process_query(
            user_id=user_id,
            session_id=session_id,
            query=query,
            bank_name=bank_name,
            language=language
        )
        
        return jsonify({
            'session_id': session_id,
            'response': response['answer'],
            'sources': response['sources'],
            'language': response['language']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/chat/new-session', methods=['POST'])
@jwt_required()
def new_session():
    """Create a new chat session"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        bank_name = data.get('bank_name')
        
        session = ChatSession(
            user_id=user_id,
            bank_name=bank_name
        )
        
        db.session.add(session)
        db.session.commit()
        
        return jsonify({
            'session': session.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/chat/sessions', methods=['GET'])
@jwt_required()
def get_sessions():
    """Get user's chat sessions"""
    try:
        user_id = get_jwt_identity()
        
        sessions = ChatSession.query.filter_by(user_id=user_id)\
            .order_by(ChatSession.created_at.desc())\
            .limit(20)\
            .all()
        
        return jsonify({
            'sessions': [session.to_dict() for session in sessions]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/banks', methods=['GET'])
@jwt_required()
def get_banks():
    """Get list of supported banks"""
    try:
        banks = banking_service.get_banks_list()
        return jsonify({'banks': banks}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/search-locations', methods=['POST'])
@jwt_required()
def search_locations():
    """Search for bank branches and ATMs"""
    try:
        data = request.get_json()
        query = data.get('query')
        bank_name = data.get('bank_name')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        results = banking_service.search_bank_locations(query, bank_name)
        
        return jsonify({'locations': results}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
