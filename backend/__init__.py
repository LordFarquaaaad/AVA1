from flask import Flask, send_from_directory, render_template
from flask_cors import CORS
from backend.extensions import db, migrate, oauth, cors
from backend.blueprints.auth import auth_bp
from backend.blueprints.email import email_bp
from backend.blueprints.google_classroom import classroom_bp  # ✅ Import Blueprint
from backend.blueprints.reports import reports_bp
from backend.blueprints.main import main_bp
from dotenv import load_dotenv
import os


load_dotenv()##

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, OPENAI_API_KEY) 
def create_app():
    # Correct path for 'templates' and 'static' inside the 'backend' directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current folder (backend/)
    template_dir = os.path.join(backend_dir, 'templates')  # Join with 'templates'
    static_dir = os.path.join(backend_dir, 'static')  # Join with 'static'
    app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)

    print(f"📂 Templates Path: {app.template_folder}")
    print(f"📂 Static Path: {app.static_folder}")

    # Initialize extensions (leave this as it is)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object("backend.config.Config")
    db.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app)

    # Register Blueprints (leave this as it is)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(email_bp, url_prefix="/email")
    app.register_blueprint(classroom_bp, url_prefix="/classroom")
    app.register_blueprint(reports_bp, url_prefix="/reports")
    app.register_blueprint(main_bp)

    # Serve Flask's homepage at `/`
    @app.route("/")
    def home():
        return render_template("home.html")  # Your existing Flask home page

    @app.route("/app", defaults={"path": ""})
    @app.route("/app/<path:path>")
    def serve_react(path):
        react_build_path = os.path.join(app.static_folder, path)

        # Ensure correct serving of static files
        if path and os.path.exists(react_build_path):
            return send_from_directory(app.static_folder, path)
    
        # Serve index.html for unmatched routes
        return send_from_directory(app.static_folder, "index.html")

    return app










