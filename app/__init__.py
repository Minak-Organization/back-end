from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__, static_folder="static")
    app.config.from_object("app.config.Config")

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.models import User, Playlist, Song
    from app.routes.auth import auth_bp
    from app.routes.playlists import playlist_bp
    from app.routes.songs import songs_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(playlist_bp)
    app.register_blueprint(songs_bp)

    @app.route("/audio/<filename>")
    def serve_audio(filename):
        from flask import send_from_directory
        import os
        audio_dir = os.path.join(os.getcwd(), "static", "audio")
        return send_from_directory(audio_dir, filename)

    # Global CORS headers
    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
        return response

    return app