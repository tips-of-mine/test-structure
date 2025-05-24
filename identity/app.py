# identity/app.py
import os
from flask import Flask
from .models import db
# Import specific config values needed by the app factory
from .config import SQLALCHEMY_DATABASE_URI, DEBUG, SECRET_KEY, APP_URL 

# Import blueprints
from .controllers import auth_bp 

def create_app():
    app = Flask(__name__)

    # Load configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = SECRET_KEY
    # Other configurations from config.py can be loaded as needed
    # For example: app.config['APP_URL'] = APP_URL
    
    # Set debug mode from config
    app.debug = DEBUG 

    db.init_app(app)

    # Create database tables if they don't exist.
    # This is usually done once, perhaps via a CLI command in more complex setups.
    # For development, doing it on startup within app_context is convenient.
    with app.app_context():
        db.create_all()
        # print("Database tables checked/created within app_context.") # Optional: can be noisy

    @app.route('/')
    def home():
        return f"Welcome to the Pulsur Identity Service! App URL: {APP_URL}"

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth') 
    # Example: /auth/register, /auth/login etc.
        
    return app

if __name__ == '__main__':
    # This block is for direct execution (e.g., python identity/app.py)
    # In production, a WSGI server like Gunicorn or uWSGI is used.
    current_app = create_app()
    port = int(os.getenv('FLASK_RUN_PORT', 5001)) # Ensure port is an integer
    print(f"Starting Identity service on port {port} with debug mode: {current_app.debug}")
    current_app.run(host='0.0.0.0', port=port)
