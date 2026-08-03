from flask import Blueprint, jsonify, g

from memory import clear_memory
from auth import login_required


system_bp = Blueprint(
    "system",
    __name__
)


@system_bp.route("/", methods=["GET"])
def home():

    return jsonify({

        "success": True,

        "message": "AI Study Assistant Backend Running"

    })


@system_bp.route("/health", methods=["GET"])
def health():

    return jsonify({

        "success": True,

        "status": "healthy"

    })


@system_bp.route("/reset", methods=["POST"])
@login_required
def reset():

    clear_memory(user_id=g.user_id)

    return jsonify({

        "success": True,

        "message": "Conversation history cleared."

    })