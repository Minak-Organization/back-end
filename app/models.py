from app import db
from flask import request

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    playlists = db.relationship("Playlist", backref="user", cascade="all, delete")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username
        }