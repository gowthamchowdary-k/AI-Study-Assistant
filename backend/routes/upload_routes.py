from flask import Blueprint, request, jsonify, g

from services.upload_service import upload_document
from services.document_service import total_documents
from auth import login_required

upload_bp = Blueprint(
    "upload",
    __name__
)


@upload_bp.route("/upload", methods=["POST"])
@login_required
def upload():

    if "file" not in request.files:
        print("UPLOAD ERROR: No file found in request.")

        return jsonify({
            "success": False,
            "error": "No file uploaded."
        }), 400

    file = request.files["file"]

    if file.filename == "":
        print("UPLOAD ERROR: Empty filename.")

        return jsonify({
            "success": False,
            "error": "No file selected."
        }), 400

    try:

        filename = upload_document(file, user_id=g.user_id)

        return jsonify({
            "success": True,
            "message": "Document uploaded and indexed successfully.",
            "file": filename,
            "documentsIndexed": total_documents(g.user_id)
        })

    except ValueError as e:

        print("=" * 60)
        print(f"UPLOAD ERROR (ValueError) for User {g.user_id}")
        print(str(e))
        print("=" * 60)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:

        import traceback

        print("=" * 60)
        print(f"UPLOAD ERROR (Exception) for User {g.user_id}")
        traceback.print_exc()
        print("=" * 60)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500