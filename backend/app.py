from flask import Flask
from flask_cors import CORS
from config import Config
from models.user import db
from flask_jwt_extended import JWTManager

# Import blueprints
from routes.auth import auth_bp
from routes.chat import chat_bp
from routes.updates import updates_bp
from routes.location import location_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    jwt = JWTManager(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(chat_bp, url_prefix='/api')
    app.register_blueprint(updates_bp, url_prefix='/api')
    app.register_blueprint(location_bp, url_prefix='/api')
    
    # Health check
    @app.route('/api/health')
    def health():
        return {'status': 'healthy', 'message': 'Banking Chatbot API is running'}
    
    # Print registered routes for debugging
    print("\n" + "="*60)
    print("REGISTERED ROUTES:")
    print("="*60)
    for rule in app.url_map.iter_rules():
        if 'location' in str(rule):
            print(f"✓ {rule.endpoint}: {rule.rule} [{', '.join(rule.methods - {'HEAD', 'OPTIONS'})}]")
    print("="*60 + "\n")
    
    return app

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
