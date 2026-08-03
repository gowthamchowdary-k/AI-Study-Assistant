from flask import Blueprint, jsonify, g

from services.document_service import (
    list_documents,
    delete_document
)
from auth import login_required


document_bp = Blueprint(
    "documents",
    __name__
)


@document_bp.route("/documents", methods=["GET"])
@login_required
def get_documents():
    """
    Returns all uploaded documents for the logged in user.
    """

    documents = list_documents(user_id=g.user_id)

    return jsonify({

        "success": True,

        "count": len(documents),

        "documents": documents

    })


@document_bp.route("/documents/<filename>", methods=["DELETE"])
@login_required
def remove_document(filename):
    """
    Deletes a document for the logged in user.
    """

    try:

        deleted_file = delete_document(filename, user_id=g.user_id)

        return jsonify({

            "success": True,

            "message": f"{deleted_file} deleted successfully."

        })

    except FileNotFoundError as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 404

    except Exception as e:

        print(e)

        return jsonify({

            "success": False,

            "error": "Unable to delete document."

        }), 500