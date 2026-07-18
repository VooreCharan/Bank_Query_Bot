from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
import logging

logger = logging.getLogger(__name__)

def token_required(f):
    """
    Decorator to protect routes that require authentication.
    Uses Flask-JWT-Extended for token verification.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Token verification failed: {str(e)}")
            return jsonify({'error': 'Invalid or missing token'}), 401
    
    return decorated

def admin_required(f):
    """
    Decorator to protect routes that require admin privileges.
    Checks if the user has admin role in JWT claims.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            claims = get_jwt()
            
            if not claims.get('is_admin', False):
                return jsonify({'error': 'Admin access required'}), 403
            
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Admin verification failed: {str(e)}")
            return jsonify({'error': 'Unauthorized access'}), 401
    
    return decorated

def validate_request_data(*required_fields):
    """
    Decorator to validate that required fields are present in request JSON.
    
    Usage:
        @validate_request_data('username', 'email', 'password')
        def register():
            # Your code here
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Content-Type must be application/json'}), 400
            
            data = request.get_json()
            missing_fields = [field for field in required_fields if field not in data or not data[field]]
            
            if missing_fields:
                return jsonify({
                    'error': f'Missing required fields: {", ".join(missing_fields)}'
                }), 400
            
            return f(*args, **kwargs)
        
        return decorated
    return decorator

def rate_limit(max_requests=100, window_seconds=3600):
    """
    Simple rate limiting decorator.
    Limits number of requests per IP address within a time window.
    
    Note: For production, use Redis-based rate limiting like Flask-Limiter
    """
    request_counts = {}
    
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            from time import time
            
            # Get client IP
            client_ip = request.remote_addr
            current_time = time()
            
            # Clean old entries
            request_counts[client_ip] = [
                timestamp for timestamp in request_counts.get(client_ip, [])
                if current_time - timestamp < window_seconds
            ]
            
            # Check rate limit
            if len(request_counts.get(client_ip, [])) >= max_requests:
                return jsonify({
                    'error': 'Rate limit exceeded. Please try again later.'
                }), 429
            
            # Add current request
            if client_ip not in request_counts:
                request_counts[client_ip] = []
            request_counts[client_ip].append(current_time)
            
            return f(*args, **kwargs)
        
        return decorated
    return decorator

def log_request(f):
    """
    Decorator to log incoming requests for monitoring and debugging.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        logger.info(f"Request: {request.method} {request.path}")
        logger.info(f"Headers: {dict(request.headers)}")
        
        if request.is_json:
            # Don't log sensitive data like passwords
            data = request.get_json()
            safe_data = {k: v for k, v in data.items() if k not in ['password', 'token']}
            logger.info(f"Body: {safe_data}")
        
        response = f(*args, **kwargs)
        logger.info(f"Response status: {response[1] if isinstance(response, tuple) else 200}")
        
        return response
    
    return decorated

def handle_exceptions(f):
    """
    Decorator to handle exceptions and return proper error responses.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logger.error(f"ValueError in {f.__name__}: {str(e)}")
            return jsonify({'error': 'Invalid input data'}), 400
        except KeyError as e:
            logger.error(f"KeyError in {f.__name__}: {str(e)}")
            return jsonify({'error': f'Missing key: {str(e)}'}), 400
        except Exception as e:
            logger.error(f"Unexpected error in {f.__name__}: {str(e)}", exc_info=True)
            return jsonify({'error': 'An unexpected error occurred'}), 500
    
    return decorated

def require_verified_email(f):
    """
    Decorator to ensure user has verified their email.
    Requires email_verified field in User model.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            
            from models.user import User
            user = User.query.filter_by(public_id=user_id).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Uncomment when email verification is implemented
            # if not user.email_verified:
            #     return jsonify({'error': 'Email verification required'}), 403
            
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Email verification check failed: {str(e)}")
            return jsonify({'error': 'Verification failed'}), 401
    
    return decorated
