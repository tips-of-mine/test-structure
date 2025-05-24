# interface/tests/test_iam.py
import unittest
import json
import uuid # For generating unique IDs in tests
from interface.app import create_app # Adjusted import for interface app
from interface.models import db, ClientUser # Assuming models are in interface.models
# Import the actual config for the interface app to be used as a base for TestConfig
from interface import config as app_config 

# Use a separate testing configuration
class TestConfig:
    TESTING = True
    # Use in-memory SQLite for tests for this service too
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Use interface specific keys from its own config, or define test specific ones
    SECRET_KEY = app_config.SECRET_KEY # Or 'test_interface_secret_key'
    DEBUG = True
    APP_URL = app_config.APP_URL # Or 'http://localhost:5002/test'
    
    # Mocked or test-specific values for external service connections
    IDENTITY_SERVICE_URL = "http://mock-identity-server:5001" 
    IDENTITY_SERVICE_AUTH_TOKEN = "test_token_for_identity_service"
    API_SECURITY_TOKEN = "test_interface_api_token" # Token this service might use
    SUPPORT_SITE_URL = app_config.SUPPORT_SITE_URL


class IAMTestCase(unittest.TestCase):

    def setUp(self):
        # Create a new app instance for each test, using TestConfig
        self.app = create_app(config_module=TestConfig)
        self.client = self.app.test_client()

        # Create all database tables within the app context
        with self.app.app_context():
            db.create_all()
            
            # It might be useful to pre-populate a 'Principal' user for some tests
            # This 'Principal' user would be the one creating other ClientUsers.
            # For now, we'll assume managing_principal_id is passed directly in test payloads.
            # Example:
            # self.managing_principal = ClientUser(id='principal-uuid-123', email='principal@example.com', client_role='Principal')
            # db.session.add(self.managing_principal)
            # db.session.commit()


    def tearDown(self):
        # Clean up the database
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_01_create_client_user_success_stub(self):
        # Test successful client user creation (currently stubs the call to Identity service)
        # This test assumes that the 'managing_principal_id' is valid and would be
        # derived from an authenticated session in a real app. Here, we pass it directly.
        managing_principal_test_id = str(uuid.uuid4()) # Simulate a principal user ID existing
        
        # First, create the managing principal user if not done globally in setUp
        with self.app.app_context():
            principal = ClientUser(id=managing_principal_test_id, email='manager@corp.com', client_role='Principal', is_active_in_interface=True)
            db.session.add(principal)
            db.session.commit()

        user_data = {
            "email": "newclientuser@corp.com",
            "client_role": "Analyst",
            "managing_principal_id": managing_principal_test_id, # This user creates the new one
            "global_role": "User", # Role for Identity Service
            "global_subscription_type": "Basic", # Subscription for Identity Service
            "company_name": "Test Corp Inc." # Company for Identity Service
        }
        response = self.client.post('/iam/users', 
                                    data=json.dumps(user_data), 
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 201, f"Response data: {response.get_data(as_text=True)}")
        json_response = response.get_json()
        self.assertIn("client_user_id", json_response)
        self.assertIn("identity_user_id", json_response) # From simulated sync
        self.assertEqual(json_response["message"], "Client user created and synced successfully (simulated)")

        # Verify user is in the Interface DB
        with self.app.app_context():
            client_user = ClientUser.query.filter_by(email="newclientuser@corp.com").first()
            self.assertIsNotNone(client_user)
            self.assertEqual(client_user.client_role, "Analyst")
            self.assertEqual(client_user.managing_principal_id, managing_principal_test_id)
            self.assertIsNotNone(client_user.identity_user_id) # Check that simulated ID was stored

    def test_02_list_client_users_stub(self):
        # Test listing client users (stub, assumes managing_principal_id is passed as query param)
        managing_principal_test_id = str(uuid.uuid4())
        
        with self.app.app_context():
            # Create a principal user
            principal = ClientUser(id=managing_principal_test_id, email='listmanager@corp.com', client_role='Principal')
            db.session.add(principal)
            # Create some users managed by this principal
            user1 = ClientUser(email='c_user1@corp.com', client_role='Viewer', managing_principal_id=managing_principal_test_id)
            user2 = ClientUser(email='c_user2@corp.com', client_role='Editor', managing_principal_id=managing_principal_test_id)
            db.session.add_all([user1, user2])
            db.session.commit()

        response = self.client.get(f'/iam/users?managing_principal_id={managing_principal_test_id}')
        self.assertEqual(response.status_code, 200, f"Response data: {response.get_data(as_text=True)}")
        json_response = response.get_json()
        self.assertIsInstance(json_response, list)
        self.assertEqual(len(json_response), 2)
        # Check for emails or other properties to confirm correct users are returned
        emails_returned = [user['email'] for user in json_response]
        self.assertIn('c_user1@corp.com', emails_returned)
        self.assertIn('c_user2@corp.com', emails_returned)

    def test_03_create_client_user_missing_fields(self):
        user_data = {
            # "email": "missingfields@corp.com", # Email is missing
            "client_role": "Analyst",
            "managing_principal_id": str(uuid.uuid4()) 
        }
        response = self.client.post('/iam/users', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        json_response = response.get_json()
        self.assertIn("Email and managing_principal_id are required", json_response["error"])

    def test_04_create_client_user_duplicate_email_in_interface(self):
        managing_principal_test_id = str(uuid.uuid4())
        with self.app.app_context():
            principal = ClientUser(id=managing_principal_test_id, email='dupmanager@corp.com', client_role='Principal')
            db.session.add(principal)
            db.session.commit()
            
        user_data = {
            "email": "duplicate_in_interface@corp.com",
            "client_role": "Analyst",
            "managing_principal_id": managing_principal_test_id,
        }
        # First creation should succeed
        response1 = self.client.post('/iam/users', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response1.status_code, 201)

        # Second attempt with same email should fail
        response2 = self.client.post('/iam/users', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response2.status_code, 409) # Conflict
        json_response = response2.get_json()
        self.assertIn("User with this email already exists in this client interface", json_response["error"])


# This allows running the tests directly using `python interface/tests/test_iam.py`
if __name__ == '__main__':
    # import uuid # Needs to be available if running directly for the default managing_principal_id
    # No, uuid is already imported at the top level of the file.
    unittest.main()
