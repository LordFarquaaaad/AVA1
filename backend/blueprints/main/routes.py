from flask import render_template
from backend.blueprints.main import main_bp

@main_bp.route("/")
def home():
    return render_template("home.html", title="Home")
