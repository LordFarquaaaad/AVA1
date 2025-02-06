from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import json

# Initialize SQLAlchemy for database management
db = SQLAlchemy()
migrate = Migrate()

# Token and credentials file paths
TOKEN_PATH = "config/token.json"
CREDENTIALS_PATH = "config/credentials.json"

# OAuth instance
oauth = OAuth()

def init_oauth(app):
    """Initialize OAuth for Google authentication."""
    oauth.init_app(app)

    # Google OAuth Configuration
    oauth.register(
        name="google",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),  # Load from environment variables
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        access_token_url="https://oauth2.googleapis.com/token",
        client_kwargs={
            "scope": "https://www.googleapis.com/auth/classroom.courses.readonly",
            "redirect_uri": "http://127.0.0.1:5000/auth/callback"  # Ensure this matches Google Cloud Console
        },
    )

def get_google_credentials():
    """Retrieve stored credentials or trigger authentication flow if missing."""
    creds = None

    print("🔍 Checking for existing token.json...")

    # ✅ Step 1: Try loading existing credentials
    if os.path.exists(TOKEN_PATH):
        try:
            with open(TOKEN_PATH, "r") as token_file:
                token_data = json.load(token_file)
                creds = Credentials.from_authorized_user_info(token_data)
            print("✅ Loaded existing credentials.")

            # ✅ Step 2: Return credentials if they are valid
            if creds and creds.valid:
                print("✅ Credentials are valid. Using stored token.")
                return creds
            else:
                print("⚠️ Stored credentials are invalid or expired. Reauthentication required.")

        except Exception as e:
            print(f"❌ Error loading token: {e}. Reauthentication required.")

    # 🚨 Step 3: If no valid credentials, just return None (DO NOT trigger OAuth here)
    print("❌ No valid credentials found. Returning None.")
    return None




