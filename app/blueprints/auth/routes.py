from flask import Blueprint, redirect, url_for, session
from app.extensions import oauth

auth_bp = Blueprint("auth", __name__)

# Login route - Redirect to Google OAuth
@auth_bp.route("/login")
def login():
    return oauth.google.authorize_redirect(url_for("auth.callback", _external=True))

# OAuth callback route
@auth_bp.route("/callback")
def callback():
    token = oauth.google.authorize_access_token()
    session["google_token"] = token
    return redirect(url_for("classroom.sync_data"))



