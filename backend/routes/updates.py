from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.banking_data_service import BankingDataService

updates_bp = Blueprint('updates', __name__)
banking_service = BankingDataService()

@updates_bp.route('/updates', methods=['GET'])
@jwt_required()
def get_updates():
    """Get latest banking updates"""
    try:
        category = request.args.get('category', 'all')
        limit = int(request.args.get('limit', 20))
        
        updates = banking_service.fetch_latest_updates(category, limit)
        
        return jsonify({
            'updates': updates,
            'count': len(updates)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@updates_bp.route('/updates/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Get available update categories"""
    try:
        categories = [
            {'id': 'all', 'name': 'All Updates'},
            {'id': 'loans', 'name': 'Loan Updates'},
            {'id': 'rbi', 'name': 'RBI Updates'},
            {'id': 'farmers', 'name': 'Farmer Schemes'},
            {'id': 'insurance', 'name': 'Insurance Updates'},
            {'id': 'general', 'name': 'General Banking'}
        ]
        
        return jsonify({'categories': categories}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
