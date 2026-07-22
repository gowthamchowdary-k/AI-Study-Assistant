from flask import Blueprint, request, jsonify

from services.upload_service import upload_pdf
from services.document_service import total_documents

upload_bp = Blueprint(
    "upload",
    __name__
)


@upload_bp.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:
        print("UPLOAD ERROR: No file found in request.")

        return jsonify({
            "success": False,
            "error": "No PDF uploaded."
        }), 400

    file = request.files["file"]

    if file.filename == "":
        print("UPLOAD ERROR: Empty filename.")

        return jsonify({
            "success": False,
            "error": "No PDF selected."
        }), 400

    try:

        filename = upload_pdf(file)

        return jsonify({
            "success": True,
            "message": "PDF uploaded successfully.",
            "file": filename,
            "documentsIndexed": total_documents()
        })

    except ValueError as e:

        print("=" * 60)
        print("UPLOAD ERROR (ValueError)")
        print(str(e))
        print("=" * 60)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:

        import traceback

        print("=" * 60)
        print("UPLOAD ERROR (Exception)")
        traceback.print_exc()
        print("=" * 60)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500