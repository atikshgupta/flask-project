from flask import Blueprint
bp = Blueprint("blueprint_example", __name__)

@bp.route("/eg_bp")
def index():
    return "this is a blueprint"