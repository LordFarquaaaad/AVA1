from flask import request, jsonify
from backend.blueprints.email import email_bp

@email_bp.route("/summarize", methods=["POST"])
def summarize():
    """Summarize an email using AI"""
    data = request.json
    email_text = data.get("email_text")
    summary = summarize_email(email_text)
    return jsonify({"summary": summary})
