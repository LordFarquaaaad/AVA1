from flask import Blueprint

reports_bp = Blueprint("reports", __name__)  # Define the reports blueprint

from . import routes  # Import routes so they're attached to the blueprint

