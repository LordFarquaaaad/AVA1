from flask import jsonify
from app.blueprints.google_classroom import classroom_bp
from .controllers import fetch_classroom_data

@classroom_bp.route("/sync", methods=["GET"])
def sync_classroom():
    """Fetch Google Classroom data and return it"""
    data = fetch_classroom_data()
    return jsonify({"classroom_data": data})
