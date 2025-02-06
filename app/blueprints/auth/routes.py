from flask import Blueprint, redirect, url_for, request, render_template
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from app.blueprints.auth import auth_bp
from app.blueprints.google_classroom.controllers import fetch_classroom_data
import json
import os

TOKEN_PATH = "config/token.json"  # Ensure this is consistent across the app

# Allow HTTP during local development
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.coursework.me",
    "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly"
]


@auth_bp.route("/login")
def authenticate():
    """Start the OAuth flow."""
    flow = InstalledAppFlow.from_client_secrets_file("config/credentials.json", SCOPES)
    flow.redirect_uri = "http://127.0.0.1:5000/auth/callback"

    # Generate the authorization URL
    auth_url, _ = flow.authorization_url(prompt="consent")

    # Render the login page with the generated auth_url
    return render_template("login.html", auth_url=auth_url)



@auth_bp.route("/callback")
def auth_callback():
    """Handle the OAuth callback and retrieve credentials."""
    # Initialize the OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file("config/credentials.json", SCOPES)
    flow.redirect_uri = "http://127.0.0.1:5000/auth/callback"

    # Fetch the authorization response from the request URL
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Retrieve the credentials object
    credentials = flow.credentials

    # Save the credentials to token.json
    TOKEN_PATH = "config/token.json"
    os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
    with open(TOKEN_PATH, "w") as token_file:
        json.dump(json.loads(credentials.to_json()), token_file)
    print(f"✅ Credentials saved to {TOKEN_PATH}")

    # Redirect to the home page
    return redirect(url_for("main.home"))



@auth_bp.route("/test")
def test():
    return "Test route works!"


