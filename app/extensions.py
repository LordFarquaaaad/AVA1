from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from google.oauth2.credentials import Credentials
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize SQLAlchemy for database management
db = SQLAlchemy()

# Initialize OAuth for handling authentication
oauth = OAuth()
def init_oauth(app):
    oauth.init_app(app)

    # Google OAuth Configuration
    oauth.register(
        name="google",
        client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_CLIENT_SECRET",
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        authorize_params=None,
        access_token_url="https://oauth2.googleapis.com/token",
        access_token_params=None,
        client_kwargs={"scope": "https://www.googleapis.com/auth/classroom.courses.readonly"},
    )
# Placeholder for Google OAuth credentials
google_credentials = None

migrate = Migrate()