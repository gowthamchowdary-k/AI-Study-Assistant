from flask import Blueprint, jsonify

from services.document_service import (
    list_documents,
    delete_document
)


document_bp = Blueprint(
    "documents",
    __name__
)


@document_bp.route("/documents", methods=["GET"])
def get_documents():
    """
    Returns all uploaded PDF documents.
    """

    documents = list_documents()

    return jsonify({

        "success": True,

        "count": len(documents),

        "documents": documents

    })


@document_bp.route("/documents/<filename>", methods=["DELETE"])
def remove_document(filename):
    """
    Deletes a document.
    """

    try:

        deleted_file = delete_document(filename)

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