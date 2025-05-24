# interface/controllers.py
from flask import Blueprint, request, jsonify
# Ensure correct relative import for models and config based on standard Flask structure
from .models import db, ClientUser 
from . import config as app_config 
import requests # For making API calls to the Identity service
import uuid # For generating IDs if needed locally before syncing

# Create a Blueprint for IAM routes within the Interface app
iam_bp = Blueprint('iam_bp', __name__)

@iam_bp.route('/users', methods=['POST'])
def create_client_user():
    # This endpoint is for a 'Principal' user to create other users within their organization.
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input, JSON data expected"}), 400

    email = data.get('email')
    client_role = data.get('client_role') 
    managing_principal_id = data.get('managing_principal_id') 

    if not email or not managing_principal_id:
        return jsonify({"error": "Email and managing_principal_id are required"}), 400

    if ClientUser.query.filter_by(email=email).first():
        return jsonify({"error": "User with this email already exists in this client interface"}), 409

    new_client_user = ClientUser(
        email=email,
        client_role=client_role,
        managing_principal_id=managing_principal_id,
        is_active_in_interface=True 
    )
    
    try:
        db.session.add(new_client_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error creating client user in local DB: {e}")
        return jsonify({"error": "Failed to create client user locally"}), 500

    identity_service_payload = {
        "email": new_client_user.email,
        "role": data.get("global_role", "User"), 
        "subscription_type": data.get("global_subscription_type", "Basic"), 
        "company_name": data.get("company_name", None), 
    }

    headers = {
        "Authorization": f"Bearer {app_config.IDENTITY_SERVICE_AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    identity_service_url = f"{app_config.IDENTITY_SERVICE_URL}/auth/register" 

    try:
        # SIMULATING API Call to Identity Service
        print(f"SIMULATING API Call to Identity Service: URL={identity_service_url}, Payload={identity_service_payload}, Headers={headers}")
        # response = requests.post(identity_service_url, json=identity_service_payload, headers=headers, timeout=10)
        # response.raise_for_status() 
        # identity_user_data = response.json()
        # new_client_user.identity_user_id = identity_user_data.get("user_id")
        
        simulated_identity_user_id = str(uuid.uuid4()) # Simulate getting an ID back
        new_client_user.identity_user_id = simulated_identity_user_id
        db.session.commit()
        print(f"Successfully synced with Identity Service (simulated). User ID: {simulated_identity_user_id}")

    except requests.exceptions.RequestException as e: # This would catch errors from the actual requests.post
        print(f"Error syncing user with Identity Service: {e}")
        # Potentially roll back local user creation or mark for retry
        # db.session.delete(new_client_user)
        # db.session.commit()
        return jsonify({"error": "User created locally, but failed to sync with main Identity Service. Please contact support."}), 502 
    except Exception as e: # Catch other potential errors during simulation or commit
        db.session.rollback()
        print(f"Generic error after local user creation during identity sync simulation: {e}")
        return jsonify({"error": "A server error occurred after creating the user locally during sync simulation."}), 500


    return jsonify({
        "message": "Client user created and synced successfully (simulated)",
        "client_user_id": new_client_user.id,
        "identity_user_id": new_client_user.identity_user_id
    }), 201


@iam_bp.route('/users', methods=['GET'])
def list_client_users():
    # In a real app, get manager_id from authenticated user's session/token
    manager_id = request.args.get('managing_principal_id') 
    if not manager_id:
        return jsonify({"error": "managing_principal_id is required as a query parameter for now (in a real app, this would come from auth)."}), 400

    users = ClientUser.query.filter_by(managing_principal_id=manager_id).all()
    
    user_list = [{
        "id": user.id, 
        "email": user.email, 
        "client_role": user.client_role,
        "is_active_in_interface": user.is_active_in_interface,
        "identity_user_id": user.identity_user_id,
        # Ensure created_at is not None before calling isoformat()
        "created_at": user.created_at.isoformat() if user.created_at else None 
        } for user in users]

    return jsonify(user_list), 200
