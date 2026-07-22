from flask import Blueprint, jsonify

from memory import clear_memory


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
def reset():

    clear_memory()

    return jsonify({

        "success": True,

        "message": "Conversation history cleared."

    })