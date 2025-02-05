from flask import Flask
from app.extensions import db, migrate, oauth
from app.blueprints.auth import auth_bp
from app.blueprints.email import email_bp
from app.blueprints.google_classroom import classroom_bp
from app.blueprints.reports import reports_bp
from app.blueprints.main import main_bp

def create_app():
    app = Flask(__name__, template_folder="../templates")
    
    # Load configurations
    app.config.from_object("app.config.Config")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)  # Tie Flask-Migrate to the app and database
    oauth.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(email_bp, url_prefix="/email")
    app.register_blueprint(classroom_bp, url_prefix="/classroom")
    app.register_blueprint(reports_bp, url_prefix="/reports")
    app.register_blueprint(main_bp)

    print("Template search path:", app.jinja_loader.searchpath)

    return app


