# interface/models.py
from flask_sqlalchemy import SQLAlchemy
import uuid # For unique IDs

db = SQLAlchemy()

class ClientUser(db.Model):
    __tablename__ = 'client_users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    # Link to the main user ID from the Identity service. This is crucial for relating users.
    identity_user_id = db.Column(db.String(36), nullable=True, index=True, unique=True) 
    # This ClientUser is managed by which 'Principal' user from the Identity service.
    # Storing the email of the principal might be one way, or their ID.
    managing_principal_id = db.Column(db.String(36), db.ForeignKey('client_users.id'), nullable=True, index=True) 
    
    email = db.Column(db.String(120), unique=True, nullable=False, index=True) # May or may not be same as identity_user's email
    # Role within this specific client's organization/interface (e.g., 'Analyst', 'Viewer')
    # This is distinct from the 'Principal' or 'User' role in the Identity service.
    client_role = db.Column(db.String(50), nullable=True) 
    
    # Permissions or specific settings related to the interface app for this user
    # Example: can_export_data, can_manage_widgets etc. Stored as JSON for flexibility.
    interface_permissions = db.Column(db.JSON, nullable=True) 
    
    is_active_in_interface = db.Column(db.Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationship for self-referential foreign key (Principal managing other ClientUsers)
    managed_users = db.relationship('ClientUser', backref=db.backref('manager', remote_side=[id]))

    def __repr__(self):
        return f'<ClientUser {self.email} (Identity ID: {self.identity_user_id})>'

class SurveyData(db.Model):
    __tablename__ = 'survey_data'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    # Who uploaded or is associated with this survey data (could be a ClientUser or a Principal)
    uploaded_by_client_user_id = db.Column(db.String(36), db.ForeignKey('client_users.id'), nullable=True, index=True)
    
    source_name = db.Column(db.String(200), nullable=False) # e.g., "Spring 2024 Citizen Survey"
    description = db.Column(db.Text, nullable=True)
    
    # Storing the actual data:
    # Option 1: Store raw data directly if small (e.g., JSON responses)
    raw_data = db.Column(db.JSON, nullable=True) 
    # Option 2: Store a link to the file if large (e.g., path in a file storage, S3 URL)
    file_path = db.Column(db.String(500), nullable=True) 
    
    data_type = db.Column(db.String(50), nullable=True) # e.g., 'json', 'csv_link', 'text'
    status = db.Column(db.String(50), default='pending_processing', nullable=False) # e.g., 'pending', 'processed', 'error'
    
    # Timestamps
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    processed_at = db.Column(db.DateTime, nullable=True)

    # Relationship to ClientUser who uploaded it
    uploader = db.relationship('ClientUser', backref=db.backref('uploaded_surveys', lazy='dynamic'))

    def __repr__(self):
        return f'<SurveyData {self.source_name} (ID: {self.id})>'

# Potential future models:
# class DashboardConfig(db.Model):
#     id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     client_user_id = db.Column(db.String(36), db.ForeignKey('client_users.id'), nullable=False)
#     config_name = db.Column(db.String(100), nullable=False)
#     layout_json = db.Column(db.JSON, nullable=False) # Store dashboard layout
#     user = db.relationship('ClientUser', backref=db.backref('dashboards', lazy='dynamic'))

# class WidgetConfig(db.Model):
#     id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
#     widget_type = db.Column(db.String(50), nullable=False) # e.g., 'persona_bubbles', 'mood_o_meter'
#     settings_json = db.Column(db.JSON, nullable=True) # Store widget specific settings
#     dashboard_id = db.Column(db.String(36), db.ForeignKey('dashboard_config.id'), nullable=True)
#     dashboard = db.relationship('DashboardConfig', backref=db.backref('widgets', lazy='dynamic'))
