# identity/config.py
import os

# Application access URL (e.g., from environment variable or hardcoded for dev)
APP_URL = os.getenv("IDENTITY_APP_URL", "https://identity.pulsur.com")

# Database Configuration
# Options: "postgresql", "sqlite"
# For production, "postgresql" is recommended.
# SQLite can be used for local development if DB_CONNECTION_STRING is not set.
DB_TYPE = os.getenv("DB_TYPE", "sqlite")

# Option 1: Individual components (primarily for PostgreSQL)
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOSTNAME = os.getenv("DB_HOSTNAME") # e.g., 'localhost' or an IP address
DB_PORT = os.getenv("DB_PORT", "5432") # Default PostgreSQL port
DB_NAME = os.getenv("DB_NAME")

# Option 2: Full connection string (takes precedence if set)
# Example for PostgreSQL: "postgresql://user:password@host:port/dbname"
# Example for SQLite: "sqlite:///./identity_dev.db" (use an absolute path in production if using SQLite)
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")


# Construct database URI for SQLAlchemy based on DB_TYPE and available components
def get_database_uri():
    if DB_CONNECTION_STRING:
        return DB_CONNECTION_STRING
    
    if DB_TYPE == "postgresql":
        if DB_USERNAME and DB_PASSWORD and DB_HOSTNAME and DB_NAME:
            return f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}"
        else:
            # Fallback or error if essential PostgreSQL components are missing
            print("WARNING: PostgreSQL selected but connection details are incomplete. Service might not connect to DB.")
            return "sqlite:///./identity_dev_fallback.db" # Fallback to SQLite if critical info missing
            
    elif DB_TYPE == "sqlite":
        # For SQLite, DB_NAME can be the path to the .db file.
        # If not specified, defaults to a local file.
        return f"sqlite:///./{DB_NAME or 'identity_local.db'}"
        
    else:
        raise ValueError(f"Unsupported DB_TYPE: {DB_TYPE}. Supported types are 'postgresql' and 'sqlite'.")

SQLALCHEMY_DATABASE_URI = get_database_uri()

# Monitoring tool access URL
MONITORING_TOOL_URL = os.getenv("MONITORING_TOOL_URL", "https://uptime.pulsur.com")

# Security Token for inter-application API communication
# This should be a unique, strong token, ideally from environment variables.
API_SECURITY_TOKEN = os.getenv("IDENTITY_API_SECURITY_TOKEN", "YOUR_UNIQUE_IDENTITY_APP_TOKEN_DEV_DEFAULT")

# Flask specific settings
SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "a_very_secret_dev_key_change_me") # Essential for session management, flash messages etc.
DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ('true', '1', 't')

# JWT Settings (if using JWT for token-based auth)
# JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "another_secret_for_jwt_dev_change_me")
# JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1) # Example
