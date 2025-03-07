# backend/config.py
from flask import session
from dotenv import load_dotenv
import os
from datetime import timedelta


# Load environment variables from .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = "postgresql://ava1:422552@localhost:5432/database"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OAuth Configuration (Google)
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey123")  # Ensure a strong key

    # Session settings
    SESSION_COOKIE_SECURE = False  # True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "None"  # ✅ Needed for cross-origin cookies
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_REFRESH_EACH_REQUEST = True

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"
