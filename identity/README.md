# Pulsur - Identification Service

This service is responsible for user authentication, registration, and access control for the Pulsur platform.

## Features
- User registration (/auth/register)
- User login (to be implemented)
- Token management (to be implemented)
- Role-based access control (foundational)

## Setup and Running

### 1. Dependencies
This project uses Python with Flask. Key dependencies include:
- Flask
- Flask-SQLAlchemy
- bcrypt
- psycopg2-binary (for PostgreSQL) or other relevant database drivers.

It's recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install Flask Flask-SQLAlchemy bcrypt psycopg2-binary # Add other dependencies as needed
```
(A `requirements.txt` file will be added later for easier dependency management.)

### 2. Configuration
Configuration is managed via environment variables, which are read by `identity/config.py`.
Create a `.env` file in the `identity` directory (and ensure it's in `.gitignore` if you create one for the project root) or set these variables in your environment:

**Required for basic operation (defaults to SQLite if not all DB vars are set):**
- `FLASK_SECRET_KEY`: A strong, random string used for session security. Example: `your_very_secret_flask_key`
- `IDENTITY_API_SECURITY_TOKEN`: A unique token for inter-service API communication. Example: `your_identity_service_secret_api_token`

**Database Configuration (PostgreSQL recommended for production):**
- `DB_TYPE`: Set to `postgresql` or `sqlite`. Defaults to `sqlite`.
- If `DB_TYPE=postgresql`:
    - `DB_USERNAME`: Your PostgreSQL username.
    - `DB_PASSWORD`: Your PostgreSQL password.
    - `DB_HOSTNAME`: Database server host (e.g., `localhost`).
    - `DB_PORT`: Database server port (e.g., `5432`).
    - `DB_NAME`: The name of your PostgreSQL database.
- If `DB_TYPE=sqlite`:
    - `DB_NAME`: Name of the SQLite file (e.g., `identity_prod.db`). Defaults to `identity_local.db` if not set.
- Alternatively, you can provide a full `DB_CONNECTION_STRING`.

**Other Optional Configuration:**
- `IDENTITY_APP_URL`: The public URL of this service. Default: `https://identity.pulsur.com`
- `MONITORING_TOOL_URL`: URL for the monitoring tool. Default: `https://uptime.pulsur.com`
- `FLASK_DEBUG`: Set to `True` for development debug mode. Default: `False`.
- `FLASK_RUN_PORT`: Port for the Flask development server. Default: `5001`.


Example `.env` file content:
```env
FLASK_SECRET_KEY='a_very_long_and_random_secret_key_for_flask'
IDENTITY_API_SECURITY_TOKEN='another_super_secret_token_for_apis'

DB_TYPE='postgresql'
DB_USERNAME='pulsur_identity_user'
DB_PASSWORD='db_password'
DB_HOSTNAME='localhost'
DB_PORT='5432'
DB_NAME='pulsur_identity_db'

FLASK_DEBUG='True'
FLASK_RUN_PORT='5001'
IDENTITY_APP_URL='http://localhost:5001'
```

### 3. Running the Service (Development)
Ensure your environment variables are set or your `.env` file is in place (you might need `python-dotenv` package and code to load it in `app.py` or `config.py` for `.env` files to work automatically, or source it manually).

To run the Flask development server:
```bash
python identity/app.py
```
The service should then be accessible, for example, at `http://localhost:5001` (or your configured `IDENTITY_APP_URL` and `FLASK_RUN_PORT`). The registration endpoint would be at `http://localhost:5001/auth/register`.

### 4. Database Initialization
The application attempts to create database tables on startup (`db.create_all()`). For more complex migrations or managing schema changes in production, tools like Flask-Migrate (Alembic) would be used.

---

*Further details on API endpoints, data models, and advanced configuration will be added as development progresses.*
```
