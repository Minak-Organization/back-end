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
    
class Playlist(db.Model):
    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "songs": [song.to_dict() for song in self.songs]
        }
    
class Song(db.Model):
    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)
    audio_filename = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "audio_url": f"{request.host_url.rstrip('/')}/audio/{self.audio_filename}"
        }