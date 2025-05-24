# identity/controllers.py
from flask import Blueprint, request, jsonify
from .models import db, User
# Assuming password hashing will be done using bcrypt
# You'd typically install this with: pip install bcrypt
import bcrypt 
import datetime # For potential JWT token expiry or other time-related logic

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth_bp', __name__)

def hash_password(password):
    # Hash a password for storing.
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8') # Store as string

def check_password(hashed_password, user_password):
    # Check a stored password against one provided by user
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))

@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input, JSON data expected"}), 400

    email = data.get('email')
    password = data.get('password')
    subscription_type = data.get('subscription_type', 'Free') # Default to 'Free'
    company_name = data.get('company_name')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Validate email format (basic example)
    if "@" not in email or "." not in email:
        return jsonify({"error": "Invalid email format"}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User with this email already exists"}), 409 # 409 Conflict

    # Determine role based on subscription type
    role = "User" # Default role
    if subscription_type in ['Pro', 'Enterprise']:
        role = "Principal"
    
    hashed_pw = hash_password(password)

    new_user = User(
        email=email,
        password_hash=hashed_pw,
        role=role,
        subscription_type=subscription_type,
        company_name=company_name,
        is_active=True, # Or False if email verification is implemented
        credit=0.00 # Default credit, adjust as per business logic
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Log the error e
        print(f"Error creating user: {e}")
        return jsonify({"error": "Failed to create user due to a server error"}), 500

    # Prepare data for API transmission (placeholder for now)
    # This data would be sent to "Interface principale administration" and "Interface principale utilisateur"
    # via an internal API call using the API_SECURITY_TOKEN from config.
    user_data_for_api = {
        "id": new_user.id,
        "email": new_user.email,
        "role": new_user.role,
        "subscription_type": new_user.subscription_type,
        "company_name": new_user.company_name,
        "is_active": new_user.is_active
    }
    
    # For now, just return a success message with the user's ID (or relevant data)
    # In a real scenario, you might return a JWT token upon successful registration/login.
    return jsonify({
        "message": "User registered successfully",
        "user_id": new_user.id,
        "details_to_sync": user_data_for_api # Simulating the data payload for other services
    }), 201

# Add other auth routes like /login, /logout, /refresh_token later
