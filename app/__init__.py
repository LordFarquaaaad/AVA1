from flask import Flask, send_from_directory, render_template
from app.extensions import db, migrate, oauth, cors
from app.blueprints.auth import auth_bp
from app.blueprints.email import email_bp
from app.blueprints.google_classroom import classroom_bp  # ✅ Import Blueprint
from app.blueprints.reports import reports_bp
from app.blueprints.main import main_bp
import os

# Other imports remain as they are...

def create_app():
    template_dir = os.path.abspath("templates")
    static_dir = os.path.abspath("static")
    app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)

    print(f"📂 Templates Path: {app.template_folder}")
    print(f"📂 Static Path: {app.static_folder}")

    # Initialize extensions (leave this as it is)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object("app.config.Config")
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










