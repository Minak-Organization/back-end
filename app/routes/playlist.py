from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Playlist, Song, db

playlist_bp = Blueprint("playlists", __name__)


@playlist_bp.route("/api/playlists", methods=["GET"])
@jwt_required()
def get_playlists():
    user_id = get_jwt_identity()
    playlists = Playlist.query.filter_by(user_id=user_id).all()
    return jsonify([p.to_dict() for p in playlists])


@playlist_bp.route("/api/playlists", methods=["POST"])
@jwt_required()
def create_playlist():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_playlist = Playlist(title=data.get("title"), user_id=user_id)
    db.session.add(new_playlist)
    db.session.commit()
    return jsonify(new_playlist.to_dict()), 201


@playlist_bp.route("/api/playlists/<int:id>", methods=["PATCH"])
@jwt_required()
def rename_playlist(id):
    user_id = get_jwt_identity()
    playlist = Playlist.query.filter_by(id=id, user_id=user_id).first()
    if not playlist:
        return jsonify({"message": "Playlist not found"}), 404

    data = request.get_json()
    playlist.title = data.get("title", playlist.title)
    db.session.commit()
    return jsonify(playlist.to_dict()), 200


@playlist_bp.route("/api/playlists/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_playlist(id):
    user_id = get_jwt_identity()
    playlist = Playlist.query.filter_by(id=id, user_id=user_id).first()
    if not playlist:
        return jsonify({"message": "Playlist not found"}), 404

    db.session.delete(playlist)
    db.session.commit()
    return jsonify({"message": "Playlist deleted"}), 200


@playlist_bp.route("/api/songs/<int:song_id>", methods=["DELETE"])
@jwt_required()
def delete_song(song_id):
    song = Song.query.get(song_id)
    if not song:
        return jsonify({"message": "Song not found"}), 404

    db.session.delete(song)
    db.session.commit()
    return jsonify({"message": "Song deleted"}), 200

@playlist_bp.route("/api/songs", methods=["GET"])
@jwt_required()
def get_all_songs():
    songs = Song.query.all()
    return jsonify([song.to_dict() for song in songs]), 200