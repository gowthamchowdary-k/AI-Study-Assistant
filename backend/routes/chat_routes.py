from flask import Blueprint, request, jsonify, g
import traceback

from services.chat_service import process_chat
from memory import get_history
from auth import login_required

chat_bp = Blueprint(
    "chat",
    __name__
)


@chat_bp.route("/chat", methods=["POST"])
@login_required
def chat():

    print("\n" + "=" * 70)
    print(f"🚀 /chat endpoint called (User: {g.user_id})")
    print("=" * 70)

    try:

        data = request.get_json()

        print("📩 Raw Request Data:")
        print(data)

        if not data:
            print("❌ No JSON received")
            return jsonify({
                "success": False,
                "error": "Invalid request."
            }), 400

        question = data.get("question", "").strip()
        action_id = data.get("action_id") or data.get("action") or None

        print(f"\n👤 User Question:")
        print(question)
        print(f"🧭 Action ID:")
        print(action_id)

        if not question:
            print("❌ Empty question")
            return jsonify({
                "success": False,
                "error": "Question cannot be empty."
            }), 400

        print("\n⏳ Calling process_chat()...")

        result = process_chat(question, action_id=action_id, user_id=g.user_id)

        print("\n✅ process_chat() completed successfully")

        print("\n📄 AI Answer:")
        print(result.get("answer", ""))

        print("\n📚 Sources:")
        print(result.get("sources", []))

        print("\n📦 Chunks Retrieved:")
        print(result.get("chunksRetrieved", 0))

        print("=" * 70)

        return jsonify({
            "success": True,
            **result
        })

    except ValueError as e:

        print("\n❌ VALUE ERROR")
        traceback.print_exc()

        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:

        print("\n❌ INTERNAL SERVER ERROR")
        traceback.print_exc()

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@chat_bp.route("/history", methods=["GET"])
@login_required
def history():

    print(f"\n📜 /history endpoint called (User: {g.user_id})")

    try:

        messages = get_history(user_id=g.user_id)

        print(f"💬 Messages Found: {len(messages)}")

        return jsonify({
            "success": True,
            "messages": messages
        })

    except Exception:

        print("\n❌ HISTORY ERROR")
        traceback.print_exc()

        return jsonify({
            "success": False,
            "error": "Unable to load history."
        }), 500