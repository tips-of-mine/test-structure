# interface/config.py
import os
# from datetime import timedelta # If JWT or other time-based features are needed

# Application access URL (e.g., from environment variable or hardcoded for dev)
APP_URL = os.getenv("INTERFACE_APP_URL", "https://interface.pulsur.com")

# Database Configuration
# Options: "postgresql", "sqlite"
# For production, "postgresql" is recommended.
DB_TYPE = os.getenv("INTERFACE_DB_TYPE", "sqlite") # Prefix with INTERFACE_ to avoid collision

# Option 1: Individual components (primarily for PostgreSQL)
DB_USERNAME = os.getenv("INTERFACE_DB_USERNAME")
DB_PASSWORD = os.getenv("INTERFACE_DB_PASSWORD")
DB_HOSTNAME = os.getenv("INTERFACE_DB_HOSTNAME") # e.g., 'localhost' or an IP address
DB_PORT = os.getenv("INTERFACE_DB_PORT", "5432") # Default PostgreSQL port
DB_NAME = os.getenv("INTERFACE_DB_NAME")

# Option 2: Full connection string (takes precedence if set)
# Example for PostgreSQL: "postgresql://user:password@host:port/dbname"
# Example for SQLite: "sqlite:///./interface_prod.db"
DB_CONNECTION_STRING = os.getenv("INTERFACE_DB_CONNECTION_STRING")


# Construct database URI for SQLAlchemy based on DB_TYPE and available components
def get_database_uri():
    if DB_CONNECTION_STRING:
        return DB_CONNECTION_STRING
    
    if DB_TYPE == "postgresql":
        if DB_USERNAME and DB_PASSWORD and DB_HOSTNAME and DB_NAME:
            return f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}"
        else:
            print("WARNING (Interface App): PostgreSQL selected but connection details are incomplete. Service might not connect to DB.")
            return f"sqlite:///./{DB_NAME or 'interface_dev_fallback.db'}" # Fallback to SQLite
            
    elif DB_TYPE == "sqlite":
        return f"sqlite:///./{DB_NAME or 'interface_local.db'}" # Use INTERFACE_DB_NAME or default
        
    else:
        raise ValueError(f"Unsupported DB_TYPE for Interface App: {DB_TYPE}. Supported types are 'postgresql' and 'sqlite'.")

SQLALCHEMY_DATABASE_URI = get_database_uri()

# Security Token for inter-application API communication (e.g., when calling Identity service)
# This token is what THIS service will use to authenticate ITSELF to OTHER services.
API_SECURITY_TOKEN = os.getenv("INTERFACE_API_SECURITY_TOKEN", "YOUR_UNIQUE_INTERFACE_APP_TOKEN_DEV_DEFAULT")

# URL for the external support site
SUPPORT_SITE_URL = os.getenv("SUPPORT_SITE_URL", "https:/glpi.tips-of-mine.fr")

# Flask specific settings
SECRET_KEY = os.getenv("INTERFACE_FLASK_SECRET_KEY", "a_very_secret_dev_key_for_interface_app_change_me")
DEBUG = os.getenv("INTERFACE_FLASK_DEBUG", "False").lower() in ('true', '1', 't')

# Configuration for connecting to the Identity Service API
IDENTITY_SERVICE_URL = os.getenv("IDENTITY_SERVICE_URL", "http://localhost:5001") # Default if running locally
# This is the token the Identity service EXPECTS from this (interface) service.
# It should match one of the client tokens configured in the Identity service if it has per-client tokens,
# or the general API_SECURITY_TOKEN of the Identity service if that's how it's set up.
# For simplicity, let's assume it needs the Identity service's main API token for now.
IDENTITY_SERVICE_AUTH_TOKEN = os.getenv("IDENTITY_SERVICE_API_SECURITY_TOKEN_FOR_INTERFACE_CLIENT")


# Example: If using JWTs issued by this service for its own frontend
# JWT_SECRET_KEY = os.getenv("INTERFACE_JWT_SECRET_KEY", "interface_jwt_secret_dev_change_me")
# JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
