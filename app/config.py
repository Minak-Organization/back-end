import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-dev-key")
    UPLOAD_FOLDER = "app/static/audio"
    ALLOWED_EXTENSIONS = {"mp3"}