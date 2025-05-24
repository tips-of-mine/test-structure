# interface/app.py
import os
from flask import Flask
from .models import db 
from . import config as app_config 

# Import blueprints
from .controllers import iam_bp # Corrected import assuming controllers.py is directly in interface package
# from .controllers.dashboard import dashboard_bp # For future dashboard functionality

def create_app(config_module=app_config): 
    app = Flask(__name__)

    # Load configurations from the imported config module
    app.config['SQLALCHEMY_DATABASE_URI'] = config_module.SQLALCHEMY_DATABASE_URI
    app.config['SECRET_KEY'] = config_module.SECRET_KEY
    app.config['DEBUG'] = config_module.DEBUG
    app.config['APP_URL'] = config_module.APP_URL
    app.config['SUPPORT_SITE_URL'] = config_module.SUPPORT_SITE_URL
    app.config['IDENTITY_SERVICE_URL'] = config_module.IDENTITY_SERVICE_URL
    app.config['IDENTITY_SERVICE_AUTH_TOKEN'] = config_module.IDENTITY_SERVICE_AUTH_TOKEN
    app.config['API_SECURITY_TOKEN'] = config_module.API_SECURITY_TOKEN
    
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    
    db.init_app(app) 

    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        return f"Welcome to the Pulsur User Interface Service! App URL: {app.config.get('APP_URL')}"

    # Register Blueprints
    app.register_blueprint(iam_bp, url_prefix='/iam') 
    # Example: /iam/users
    
    # Register other blueprints as they are developed
    # app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
        
    return app

if __name__ == '__main__':
    current_app = create_app() 
    port = int(os.getenv('INTERFACE_FLASK_RUN_PORT', 5002))
    print(f"Starting User Interface service on port {port} with debug mode: {current_app.debug}")
    current_app.run(host='0.0.0.0', port=port)
