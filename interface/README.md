# Pulsur - User Interface Service

This service provides the main user-facing dashboards and tools for Pulsur clients. It handles client-side user management (IAM), data visualization, and interaction with other Pulsur services.

## Features (Planned/In-Progress)
- Client-specific user management (IAM) via `/iam` endpoints:
  - Creation of users within an organization by a "Principal" account.
  - Listing users within an organization.
- Data dashboards (personas, trends, etc. - to be implemented).
- Manual data upload capabilities (e.g., surveys - to be implemented).
- Communication with the main "Identification" service for user authentication and central user attributes.

## Setup and Running

### 1. Dependencies
This project uses Python with Flask. Key dependencies include:
- Flask
- Flask-SQLAlchemy
- requests (for inter-service communication)
- psycopg2-binary (for PostgreSQL) or other relevant database drivers.

It's recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install Flask Flask-SQLAlchemy requests psycopg2-binary # Add other dependencies as needed
```
(A `requirements.txt` file will be added later for easier dependency management.)

### 2. Configuration
Configuration is managed via environment variables, which are read by `interface/config.py`.
Create a `.env` file in the `interface` directory or set these variables in your environment:

**Required for basic operation (defaults to SQLite if not all DB vars are set):**
- `INTERFACE_FLASK_SECRET_KEY`: A strong, random string for session security. Example: `your_very_secret_interface_flask_key`
- `INTERFACE_API_SECURITY_TOKEN`: A unique token this service might use to identify itself if it exposes its own APIs to other internal services. Example: `your_interface_service_secret_api_token`

**Database Configuration (PostgreSQL recommended for production):**
- `INTERFACE_DB_TYPE`: Set to `postgresql` or `sqlite`. Defaults to `sqlite`.
- If `INTERFACE_DB_TYPE=postgresql`:
    - `INTERFACE_DB_USERNAME`: Your PostgreSQL username.
    - `INTERFACE_DB_PASSWORD`: Your PostgreSQL password.
    - `INTERFACE_DB_HOSTNAME`: Database server host (e.g., `localhost`).
    - `INTERFACE_DB_PORT`: Database server port (e.g., `5432`).
    - `INTERFACE_DB_NAME`: The name of your PostgreSQL database for this service.
- If `INTERFACE_DB_TYPE=sqlite`:
    - `INTERFACE_DB_NAME`: Name of the SQLite file (e.g., `interface_prod.db`). Defaults to `interface_local.db`.
- Alternatively, you can provide a full `INTERFACE_DB_CONNECTION_STRING`.

**Connection to Identity Service:**
- `IDENTITY_SERVICE_URL`: The base URL of the main "Identification" service. Example: `http://localhost:5001`
- `IDENTITY_SERVICE_AUTH_TOKEN`: The API token this service (Interface) uses to authenticate with the "Identification" service. This should be a token recognized and validated by the Identity service.

**Other Optional Configuration:**
- `INTERFACE_APP_URL`: The public URL of this service. Default: `https://interface.pulsur.com`
- `SUPPORT_SITE_URL`: URL for the GLPI support site. Default: `https:/glpi.tips-of-mine.fr`
- `INTERFACE_FLASK_DEBUG`: Set to `True` for development debug mode. Default: `False`.
- `INTERFACE_FLASK_RUN_PORT`: Port for the Flask development server. Default: `5002`.

Example `.env` file content for `interface` app:
```env
INTERFACE_FLASK_SECRET_KEY='a_very_long_and_random_secret_key_for_interface'
INTERFACE_API_SECURITY_TOKEN='interface_service_api_token_shhh'

INTERFACE_DB_TYPE='postgresql'
INTERFACE_DB_USERNAME='pulsur_interface_user'
INTERFACE_DB_PASSWORD='db_password_interface'
INTERFACE_DB_HOSTNAME='localhost'
INTERFACE_DB_PORT='5432'
INTERFACE_DB_NAME='pulsur_interface_db'

IDENTITY_SERVICE_URL='http://localhost:5001' # Assuming Identity service is running locally on port 5001
IDENTITY_SERVICE_AUTH_TOKEN='token_that_identity_service_expects_from_me' # This token is validated by Identity service

INTERFACE_APP_URL='http://localhost:5002'
INTERFACE_FLASK_DEBUG='True'
INTERFACE_FLASK_RUN_PORT='5002'
SUPPORT_SITE_URL='https:/glpi.tips-of-mine.fr'
```

### 3. Running the Service (Development)
Ensure your environment variables are set (e.g., via a `.env` file and `python-dotenv`, or sourced manually).

To run the Flask development server:
```bash
python interface/app.py
```
The service should then be accessible, for example, at `http://localhost:5002`. The IAM user creation endpoint would be at `http://localhost:5002/iam/users`.

### 4. Database Initialization
The application attempts to create database tables on startup (`db.create_all()`). For production, consider using Flask-Migrate (Alembic) for schema management.

---

*Further details on API endpoints, data models, frontend integration, and advanced configuration will be added as development progresses.*
```
