from flask import render_template
from datetime import datetime
from backend.blueprints.main import main_bp

@main_bp.route("/")
def home():
    return render_template("home.html", current_year=datetime.now().year)
