import sys
import io

# Set default encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from flask import Flask, send_from_directory, render_template
from flask_cors import CORS
from backend.extensions import db, migrate, oauth, login_manager
from backend.blueprints.auth import auth_bp
from backend.blueprints.email import email_bp
from backend.blueprints.google_classroom import classroom_bp
from backend.blueprints.reports import reports_bp
from backend.blueprints.main import main_bp
from backend.models import User
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Ensure required environment variables are set
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY must be set in the environment.")

def create_app():
    """Create and configure the Flask application."""
    # Define template & static folder paths
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(backend_dir, 'templates')
    static_dir = os.path.join(backend_dir, 'static')

    app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
    app.config.from_object("backend.config.Config")
    app.config['JSON_AS_ASCII'] = False  # Ensure JSON responses are UTF-8 encoded

    # Initialize Flask extensions
    CORS(app, origins=["http://localhost:3000"], supports_credentials=True)
    db.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app)
    login_manager.init_app(app)  # Ensure 'login_manager' is initialized

    # Redirect unauthorized users to login
    login_manager.login_view = "auth.login"

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(email_bp, url_prefix="/email")
    app.register_blueprint(classroom_bp, url_prefix="/classroom")
    app.register_blueprint(reports_bp, url_prefix="/reports")
    app.register_blueprint(main_bp)

    # User Loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        """Fetch the user from the database by ID."""
        return User.query.get(int(user_id))

    # Homepage route
    @app.route('/')
    def home():
        return render_template("home.html")

    # Serve React frontend
    @app.route('/app', defaults={'path': ''})
    @app.route('/app/<path:path>')
    def serve_react(path):
        react_build_path = os.path.join(app.static_folder, path)

        # Ensure correct serving of static files
        if path and os.path.exists(react_build_path):
            return send_from_directory(app.static_folder, path)

        # Serve index.html for unmatched routes
        return send_from_directory(app.static_folder, "index.html")

    return app










