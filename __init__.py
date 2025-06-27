from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config') 
    db.init_app(app)
    jwt.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.playlists import playlist_bp
    from app.routes.songs import songs_bp
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(playlist_bp, url_prefix='/api')
    app.register_blueprint(songs_bp, url_prefix='/api')

    @app.route('/')
    def home():
        return "Welcome to the Music App!"

    return app
