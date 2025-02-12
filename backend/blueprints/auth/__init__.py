from flask import Blueprint
print("Loading auth blueprint...")
auth_bp = Blueprint("auth", __name__)
print("Auth blueprint loaded!")
from . import routes  # Import routes
