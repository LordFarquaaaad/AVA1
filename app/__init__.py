from flask import Flask
from app.extensions import db, migrate, oauth
from app.blueprints.auth import auth_bp
from app.blueprints.email import email_bp
from app.blueprints.google_classroom import classroom_bp  # ✅ Import Blueprint
from app.blueprints.reports import reports_bp
from app.blueprints.main import main_bp

def create_app():
    app = Flask(__name__, template_folder="../templates")

    # Load configurations
    app.config.from_object("app.config.Config")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app)

    # ✅ Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(email_bp, url_prefix="/email")
    app.register_blueprint(classroom_bp, url_prefix="/classroom")
    app.register_blueprint(reports_bp, url_prefix="/reports")
    app.register_blueprint(main_bp)

    # ✅ Force-load Google Classroom routes
    from app.blueprints.google_classroom import routes  # 🔥 Add this line

    print("✅ Registered Blueprints:", app.blueprints.keys())  # Debugging

    return app




