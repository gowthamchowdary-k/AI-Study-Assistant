from flask import Flask
from flask_cors import CORS

from routes.chat_routes import chat_bp
from routes.upload_routes import upload_bp
from routes.document_routes import document_bp
from routes.system_routes import system_bp


def create_app():

    app = Flask(__name__)

    CORS(app)

    app.register_blueprint(chat_bp)

    app.register_blueprint(upload_bp)

    app.register_blueprint(document_bp)

    app.register_blueprint(system_bp)

    return app


app = create_app()


if __name__ == "__main__":

    print("=" * 60)
    print("📚 AI Study Assistant Backend Started")
    print("=" * 60)
    print("🌐 Server : http://127.0.0.1:5000")
    print("=" * 60)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )