import os
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from app import db
from app.models import Song

songs_bp = Blueprint("songs", __name__)

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]
    )

@songs_bp.route("/api/songs", methods=["GET"])
@jwt_required()
def get_songs():
    songs = Song.query.all()
    song_data = []
    for song in songs:
        song_data.append({
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "audio_url": f"{request.host_url.rstrip('/')}/static/audio/{song.audio_filename}"
        })
    return jsonify(song_data), 200

@songs_bp.route("/api/songs", methods=["POST"])
@jwt_required()
def upload_song():
    title = request.form.get("title")
    artist = request.form.get("artist")
    file = request.files.get("file")

    if not title or not artist or not file:
        return jsonify({"message": "Missing required fields"}), 400
    if not allowed_file(file.filename):
        return jsonify({"message": "Only .mp3 files allowed"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    new_song = Song(title=title, artist=artist, audio_filename=filename)
    db.session.add(new_song)
    db.session.commit()

    return jsonify({
        "id": new_song.id,
        "title": new_song.title,
        "artist": new_song.artist,
        "audio_url": f"{request.host_url.rstrip('/')}/static/audio/{filename}"
    }), 201

@songs_bp.route("/static/audio/<filename>")
def serve_audio(filename):
    return send_from_directory(os.path.join("static", "audio"), filename)