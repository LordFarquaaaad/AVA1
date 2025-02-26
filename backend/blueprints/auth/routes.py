from flask import Blueprint, redirect, url_for, request, render_template, jsonify
from flask_login import UserMixin, login_user, logout_user, login_required, current_user
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from backend.extensions import db
from backend.blueprints.auth import auth_bp
from backend.models import User
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash  # To securely hash passwords

TOKEN_PATH = "config/token.json"  # Ensure this is consistent across the app

# Allow HTTP during local development
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.coursework.students",
    "https://www.googleapis.com/auth/classroom.courseworkmaterials",
    "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly",
    "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly",
    "https://www.googleapis.com/auth/classroom.coursework.me",
    "https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly"
]

@auth_bp.route("/test")
def test():
    return "Test route works!"

@auth_bp.route("/authenticate")
def authenticate():
    """Start the OAuth flow."""
    flow = InstalledAppFlow.from_client_secrets_file("backend/config/credentials.json", SCOPES)
    flow.redirect_uri = "http://127.0.0.1:5000/auth/callback"

    # Generate the authorization URL
    auth_url, _ = flow.authorization_url(prompt="consent")

    # Render the login page with the generated auth_url
    return render_template("login.html", auth_url=auth_url)

@auth_bp.route("/callback")
def auth_callback():
    """Handle the OAuth callback and retrieve credentials."""
    flow = InstalledAppFlow.from_client_secrets_file("backend/config/credentials.json", SCOPES)
    flow.redirect_uri = "http://127.0.0.1:5000/auth/callback"

    # Fetch the authorization response from the request URL
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Retrieve the credentials object
    credentials = flow.credentials

    # Save the credentials to token.json
    os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
    with open(TOKEN_PATH, "w") as token_file:
        json.dump(json.loads(credentials.to_json()), token_file)
    print(f"✅ Credentials saved to {TOKEN_PATH}")

    # Redirect to the home page
    return redirect(url_for("main.home"))



@auth_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')  # ✅ Extract password correctly

        if not username or not password:
            return jsonify({'message': 'Missing required fields'}), 400

        # ✅ Create user & hash password
        new_user = User(username=username)
        new_user.set_password(password)  # ✅ Use method to hash password
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': f'User {username} created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creating user: {str(e)}'}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    print("Incoming JSON data:", request.get_json())
    
    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400  # ✅ Handle missing fields

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message": "User not found"}), 401  # ✅ Handle non-existent user

    if not user.check_password(password):  # ✅ Make sure check_password() is implemented
        return jsonify({"message": "Invalid credentials"}), 401

    

    login_user(user)
    return jsonify({"message": "Login successful", "user": {"id": user.id, "username": user.username}}), 200

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Successfully logged out'}), 200

@auth_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    return jsonify({'username': current_user.username, 'user_id': current_user.id})

@auth_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return jsonify({"message": f"Welcome {current_user.username}! Your ID is {current_user.id}."})