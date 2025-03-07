import sys
import io
import os
import logging
from flask import Flask, send_from_directory, render_template, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from backend.extensions import db, migrate, oauth
from backend.models import User
from datetime import timedelta

# ✅ Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

# ✅ Set default encoding to UTF-8 (fixes console logging issues)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# ✅ Load environment variables
load_dotenv()

# Ensure required environment variables are set
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-very-secure-secret-key")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY must be set in the environment.")
if not JWT_SECRET_KEY:
    logging.warning("JWT_SECRET_KEY not set, using insecure default. Set in environment for production.")

def create_app():
    """Create and configure the Flask application."""
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(backend_dir, "templates")
    static_dir = os.path.join(backend_dir, "static")

    app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)

    # ✅ Load all configurations first (prevents overwrites)
    app.config.from_object("backend.config.Config")

    # ✅ JWT Configuration
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token_cookie"
    app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token_cookie"

    # ✅ Enable CORS with wildcard for all routes
    CORS(
        app,
        supports_credentials=True,
        resources={r"/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
            "allow_headers": ["Content-Type", "Authorization", "Accept"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "expose_headers": ["Set-Cookie", "Authorization"],
            "max_age": 86400,
            "supports_credentials": True,
            "send_wildcard": False,
        }}
    )

    # ✅ Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app)

    # ✅ Initialize JWTManager
    jwt = JWTManager(app)

    # ✅ user_identity_loader: Convert user to string (user.id)
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        if isinstance(user, str):
            return user  # Already a string (e.g., user.id)
        if isinstance(user, dict) and "id" in user:
            return str(user["id"])  # Extract id from dict
        if hasattr(user, 'id'):
            return str(user.id)  # Convert User object to string
        raise ValueError("Invalid user object in JWT identity lookup")

    # ✅ user_lookup_loader: Load user from string identity (user.id)
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        user_id = jwt_data["sub"]
        return User.query.get(int(user_id))

    # ✅ Handle unauthorized access
    @jwt.unauthorized_loader
    def unauthorized_response(callback):
        return jsonify({"error": "Missing or invalid JWT token"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        logger.error(f"❌ Invalid JWT token: {error}")
        return jsonify({"error": "Invalid JWT token", "details": str(error)}), 422

    # ✅ Import blueprints
    from backend.blueprints.auth import auth_bp
    from backend.blueprints.email import email_bp
    from backend.blueprints.google_classroom import classroom_bp
    from backend.blueprints.reports import reports_bp
    from backend.blueprints.main import main_bp

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(email_bp, url_prefix="/email")
    app.register_blueprint(classroom_bp, url_prefix="/classroom")
    app.register_blueprint(reports_bp, url_prefix="/api/reports")
    app.register_blueprint(main_bp)

    # Debug route to confirm /auth/login registration
    @app.route("/auth/test-login", methods=["GET"])
    def test_login():
        return jsonify({"message": "Auth blueprint and /login route are registered"}), 200

    # ✅ Add a catch-all OPTIONS handler
    @app.route('/<path:path>', methods=['OPTIONS'])
    def handle_options(path):
        return jsonify({}), 200

    # ✅ Homepage route
    @app.route("/")
    def home():
        return render_template("home.html")

    # ✅ Serve React frontend
    @app.route("/app", defaults={"path": ""})
    @app.route("/app/<path:path>")
    def serve_react(path):
        react_build_path = os.path.join(app.static_folder, path)
        if path and os.path.exists(react_build_path):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, "index.html")

    # Debug: Print all routes
    print(app.url_map)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)