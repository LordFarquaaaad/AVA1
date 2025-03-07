from flask import Blueprint, redirect, url_for, request, render_template, jsonify, make_response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
    get_jwt
)
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import json
import logging
from datetime import timedelta
from werkzeug.security import check_password_hash
from email_validator import validate_email, EmailNotValidError

from backend.extensions import db
from backend.models import User
from backend.blueprints.auth import auth_bp


logger = logging.getLogger(__name__)

TOKEN_PATH = "config/token.json"
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

# Helper function for email validation
def validate_email_format(email):
    try:
        validate_email(email, check_deliverability=False)
        return True
    except EmailNotValidError:
        return False

@auth_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Missing required fields (username and password)'}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({'message': 'Username already exists'}), 400

        if email:
            if not validate_email_format(email):
                return jsonify({'message': 'Invalid email format'}), 400
            if User.query.filter_by(email=email).first():
                return jsonify({'message': 'Email already exists'}), 400

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': f'User {username} created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"🔥 Error creating user: {e}")
        return jsonify({'message': 'Error creating user', 'details': str(e)}), 500

# ✅ Login & Generate JWT Tokens
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        logger.debug(f"📥 Incoming login request: {data}")

        identifier = data.get("identifier")  # Can be username or email
        password = data.get("password")

        if not identifier or not password:
            return jsonify({"message": "Missing identifier or password"}), 400

        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier)
        ).first()

        if not user or not user.check_password(password):
            logger.warning(f"❌ Invalid credentials for {identifier}")
            return jsonify({"message": "Invalid credentials"}), 401

        # ✅ Use `user.id` as identity & attach additional claims
        additional_claims = {"username": user.username, "email": user.email}
        access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
        refresh_token = create_refresh_token(identity=str(user.id), additional_claims=additional_claims)

        # ✅ Send token both as JSON & HTTPOnly cookie
        response = jsonify({
            "message": "Login successful",
            "user": {"id": user.id, "username": user.username, "email": user.email},
            "access_token": access_token,
            "refresh_token": refresh_token
        })
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)

        logger.info(f"✅ User {user.username} logged in, JWT issued.")
        return response, 200

    except Exception as e:
        logger.error(f"🔥 ERROR in login(): {e}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@auth_bp.route("/login", methods=["GET"])
def show_login_form():
    """Serve a login form (for testing or UI-based login)"""
    
    # 🟢 If using HTML-based login (for manual testing)
    return render_template("login.html")

    # 🟢 If using React frontend, return JSON instead
    # return jsonify({"message": "Use POST /auth/login to authenticate"}), 200


# ✅ Get Logged-in User
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    try:
        logger.debug(f"📥 Incoming /auth/me request. Headers: {request.headers}")

        # ✅ Retrieve JWT Identity
        user_id = get_jwt_identity()  # This is stored as a string
        jwt_data = get_jwt()  # Extract additional claims
        logger.debug(f"JWT Identity (sub): {user_id}, Claims: {jwt_data}")

        user = User.query.get(int(user_id))  # Convert ID to integer
        if not user:
            logger.warning("❌ User not found in database for JWT identity")
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
            }
        }), 200

    except Exception as e:
        logger.error(f"❌ Error fetching user: {e}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

# ✅ Refresh JWT Access Token
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        user_id = get_jwt_identity()
        jwt_data = get_jwt()
        additional_claims = {
            "username": jwt_data["username"],
            "email": jwt_data["email"]
        }

        # Create new access and refresh tokens
        new_access_token = create_access_token(identity=user_id, additional_claims=additional_claims)
        new_refresh_token = create_refresh_token(identity=user_id)

        # Prepare response
        response = make_response(jsonify({"access_token": new_access_token, "refresh_token": new_refresh_token}), 200)

        # Set secure cookies
        response.set_cookie(
            "access_token_cookie",
            new_access_token,
            httponly=True,
            secure=False,  # Set `True` in production (for HTTPS)
            samesite="Lax",
            max_age=900,  # 15 minutes
            path="/"
        )
        response.set_cookie(
            "refresh_token_cookie",
            new_refresh_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=86400,  # 24 hours
            path="/"
        )

        return response

    except Exception as e:
        logger.error(f"❌ Error refreshing token: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500



# ✅ Logout & Clear Cookies
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({'message': 'Successfully logged out'})
    unset_jwt_cookies(response)
    logger.info("✅ User logged out.")
    return response, 200

@auth_bp.route("/authenticate")
def authenticate():
    """Start the Google OAuth flow."""
    flow = InstalledAppFlow.from_client_secrets_file("backend/config/credentials.json", SCOPES)
    flow.redirect_uri = "http://127.0.0.1:5000/auth/callback"
    auth_url, _ = flow.authorization_url(prompt="consent")
    return render_template("login.html", auth_url=auth_url)

@auth_bp.route("/callback")
def auth_callback():
    """Handle the OAuth callback, retrieve credentials, and issue JWT."""
    flow = InstalledAppFlow.from_client_secrets_file("backend/config/credentials.json", SCOPES)
    flow.redirect_uri = "http://127.0.0.1:5000/auth/callback"
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
    with open(TOKEN_PATH, "w") as token_file:
        json.dump(json.loads(credentials.to_json()), token_file)
    logger.info(f"✅ Credentials saved to {TOKEN_PATH}")

    email = credentials.id_token.get("email")
    user = User.query.filter_by(email=email).first()
    if not user:
        username = email.split("@")[0] if "@" in email else email
        user = User(username=username, email=email)
        user.set_password(os.urandom(16).hex())
        db.session.add(user)
        db.session.commit()
        logger.info(f"✅ New user {user.username} registered via OAuth")

    # Use user.id as the sub claim (string), add additional data as claims
    additional_claims = {
        "username": user.username,
        "email": user.email
    }
    logger.debug(f"Creating token for user - sub: {str(user.id)}, claims: {additional_claims}")
    access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=str(user.id), additional_claims=additional_claims)

    response = make_response(redirect(url_for("main.home")))
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    logger.info(f"✅ JWT issued for user {user.username} via OAuth")
    return response



@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    jwt_data = get_jwt()
    logger.info(f"User {jwt_data['username']} accessed profile.")
    return jsonify({
        'username': jwt_data['username'],
        'user_id': int(user_id),
        'email': jwt_data['email'] if 'email' in jwt_data else None
    })

@auth_bp.route("/dashboard", methods=["GET"])
def dashboard():
    user_id = get_jwt_identity()
    jwt_data = get_jwt()
    logger.info(f"User {jwt_data['username']} accessed dashboard")
    return jsonify({
        "message": f"Welcome {jwt_data['username']}! Your ID is {user_id}."
    })

