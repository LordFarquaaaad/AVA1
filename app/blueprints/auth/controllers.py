from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.coursework.me",
    "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly"
]

def authenticate_google():
    """Authenticate Google API with explicit redirect URI."""
    flow = InstalledAppFlow.from_client_secrets_file(
        "config/credentials.json", SCOPES
    )

    # Explicitly set the redirect URI
    flow.redirect_uri = "http://127.0.0.1:8080/"
    
    # Debug log to confirm the redirect URI being used
    print(f"Redirect URI being used: {flow.redirect_uri}")

    # Run the local server for OAuth authentication
    credentials = flow.run_local_server(port=8080)  # Match the redirect URI port

    print("✅ Authentication successful!")
    return credentials




