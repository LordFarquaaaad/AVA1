from flask import Blueprint

classroom_bp = Blueprint("classroom", __name__, url_prefix="/classroom")

from . import routes  # ✅ Ensure routes are imported
