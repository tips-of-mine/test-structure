# identity/models.py
from flask_sqlalchemy import SQLAlchemy
import uuid # For generating unique IDs if not using auto-incrementing integers primarily

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())) # Using UUID for id
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False) # Store hashed passwords, not plain text
    role = db.Column(db.String(50), nullable=False) # e.g., 'Principal', 'User', 'Admin'
    subscription_type = db.Column(db.String(50), nullable=True) # e.g., 'Free', 'Basic', 'Pro', 'Enterprise'
    company_name = db.Column(db.String(150), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    # 'credit' could mean different things (e.g., API call credits, monetary value)
    # Using Numeric for flexibility, adjust precision/scale as needed.
    credit = db.Column(db.Numeric(10, 2), default=0.00, nullable=True) 
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<User {self.email}>'

    # Add methods for password hashing and checking here later
    # e.g., set_password(self, password) and check_password(self, password)
