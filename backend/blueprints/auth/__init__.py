# backend/blueprints/auth/__init__.py
from flask import Blueprint

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")  # Add url_prefix="/auth"

from . import routes  # ✅ Import routes so they attach to the Blueprint

