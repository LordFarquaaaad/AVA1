from flask import Blueprint, render_template, jsonify
from backend.extensions import get_google_credentials
from backend.blueprints.google_classroom.controllers import sync_classroom_data
from backend.blueprints.google_classroom import classroom_bp

@classroom_bp.route("/sync-page", methods=["GET"])
def sync_page():
    return render_template("sync.html")

@classroom_bp.route("/sync", methods=["GET"])
def sync_classroom():
    """Fetch Google Classroom data and return status."""
    try:
        print("🔍 Checking stored credentials for /sync...")
        credentials = get_google_credentials()

        # 🚨 If credentials are missing or invalid, return 401
        if not credentials or not credentials.valid:
            print("❌ No valid credentials. Redirecting to login.")
            return jsonify({"error": "Google authentication required. Please log in."}), 401

        print("✅ Credentials verified. Fetching classroom data...")
        response = sync_classroom_data(credentials)
        return jsonify(response)

    except Exception as e:
        print(f"❌ Error in /sync route: {e}")
        return jsonify({"error": str(e)}), 500





