from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.location_service import LocationService
import traceback

location_bp = Blueprint('location', __name__)
location_service = LocationService()

print("✓ Location blueprint created")

@location_bp.route('/location/search', methods=['POST', 'OPTIONS'])
@jwt_required(optional=True)  # Make JWT optional for debugging
def search_banks_atms():
    """Search for banks and ATMs by location"""
    
    # Handle OPTIONS request (CORS preflight)
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        print("\n" + "="*60)
        print("[LOCATION SEARCH] Request received")
        print("="*60)
        
        # Get request data
        data = request.get_json()
        print(f"[LOCATION] Request data: {data}")
        print(f"[LOCATION] Request headers: {dict(request.headers)}")
        
        if not data:
            print("[LOCATION] ERROR: No data provided")
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        location = data.get('location')
        print(f"[LOCATION] Location string: '{location}'")
        
        if not location or not str(location).strip():
            print("[LOCATION] ERROR: Location is empty or invalid")
            return jsonify({
                'success': False,
                'error': 'Location is required and cannot be empty'
            }), 400
        
        limit = data.get('limit', 10)
        print(f"[LOCATION] Limit: {limit}")
        
        print(f"[LOCATION] Calling location service...")
        results = location_service.search_by_location(str(location).strip(), limit=int(limit))
        
        print(f"[LOCATION] Service returned: success={results.get('success')}, count={results.get('count', 0)}")
        print("="*60 + "\n")
        
        return jsonify(results), 200
        
    except Exception as e:
        print(f"[LOCATION] EXCEPTION: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@location_bp.route('/location/geocode', methods=['POST', 'OPTIONS'])
@jwt_required(optional=True)
def geocode():
    """Convert location to coordinates"""
    
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        location = data.get('location')
        
        if not location:
            return jsonify({
                'success': False,
                'error': 'Location is required'
            }), 400
        
        coords = location_service.geocode_location(location)
        
        if not coords:
            return jsonify({
                'success': False,
                'error': 'Location not found'
            }), 404
        
        return jsonify({
            'success': True,
            'coordinates': coords
        }), 200
        
    except Exception as e:
        print(f"[GEOCODE] Error: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Add a test route to verify blueprint is working
@location_bp.route('/location/test', methods=['GET'])
def test():
    """Test route to verify blueprint is registered"""
    return jsonify({
        'status': 'ok',
        'message': 'Location service is working'
    }), 200

print("✓ Location routes registered")
