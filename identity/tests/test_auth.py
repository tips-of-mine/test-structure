# identity/tests/test_auth.py
import unittest
import json
from identity.app import create_app # Adjusted import
from identity.models import db, User

# Use a separate testing configuration
# You might have a specific config class or modify the existing one for tests
class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # Use in-memory SQLite for tests
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test_secret_key'
    DEBUG = True
    # Ensure API_SECURITY_TOKEN is also set if your app logic depends on it during tests
    API_SECURITY_TOKEN = "test_api_security_token" 
    APP_URL = "http://localhost:5000" # Or any other consistent test URL


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        # Create a new app instance for each test
        self.app = create_app() 
        self.app.config.from_object(TestConfig()) # Apply test configuration
        
        self.client = self.app.test_client()

        # Create all database tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up the database
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_01_register_user_success(self):
        # Test successful user registration
        user_data = {
            "email": "testuser@example.com",
            "password": "SecurePassword123",
            "subscription_type": "Pro",
            "company_name": "TestCorp"
        }
        response = self.client.post('/auth/register', 
                                    data=json.dumps(user_data), 
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        json_response = response.get_json()
        self.assertIn("user_id", json_response)
        self.assertEqual(json_response["message"], "User registered successfully")
        self.assertEqual(json_response["details_to_sync"]["email"], "testuser@example.com")
        self.assertEqual(json_response["details_to_sync"]["role"], "Principal") # Pro subscription maps to Principal

        # Verify user is in the database
        with self.app.app_context():
            user = User.query.filter_by(email="testuser@example.com").first()
            self.assertIsNotNone(user)
            self.assertEqual(user.company_name, "TestCorp")

    def test_02_register_user_missing_fields(self):
        # Test registration with missing email
        user_data = {"password": "SecurePassword123"}
        response = self.client.post('/auth/register', 
                                    data=json.dumps(user_data), 
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        json_response = response.get_json()
        self.assertIn("Email and password are required", json_response["error"])

        # Test registration with missing password
        user_data = {"email": "anotheruser@example.com"}
        response = self.client.post('/auth/register', 
                                    data=json.dumps(user_data), 
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        json_response = response.get_json()
        self.assertIn("Email and password are required", json_response["error"])

    def test_03_register_user_duplicate_email(self):
        # First registration
        user_data = {
            "email": "duplicate@example.com",
            "password": "SecurePassword123",
            "subscription_type": "Free"
        }
        response = self.client.post('/auth/register', 
                                    data=json.dumps(user_data), 
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201) # Ensure first one succeeds

        # Attempt to register with the same email
        response_duplicate = self.client.post('/auth/register', 
                                              data=json.dumps(user_data), 
                                              content_type='application/json')
        self.assertEqual(response_duplicate.status_code, 409) # 409 Conflict
        json_response = response_duplicate.get_json()
        self.assertIn("User with this email already exists", json_response["error"])

# This allows running the tests directly using `python identity/tests/test_auth.py`
if __name__ == '__main__':
    unittest.main()
