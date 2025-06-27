import os
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User
from app import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"message": "Missing credentials"}), 400

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            return jsonify({"message": "Invalid username or password"}), 401

        access_token = create_access_token(identity=str(user.id))
        return jsonify({"token": access_token}), 200

    except Exception as e:
        print("🚨 Login route error:", str(e))
        return jsonify({"message": "Internal server error"}), 500


@auth_bp.route("/api/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()

        if not username or not password:
            return jsonify({"message": "Username and password required"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"message": "Username already exists"}), 409

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        print("🚨 Registration error:", str(e))
        return jsonify({"message": "Internal server error"}), 500


@auth_bp.route("/api/profile", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.to_dict()), 200


@auth_bp.route("/api/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        data = request.get_json()
        new_username = data.get("username", "").strip()
        new_email = data.get("email", "").strip()

        if new_username and new_username != user.username:
            if User.query.filter_by(username=new_username).first():
                return jsonify({"message": "Username already taken"}), 409
            user.username = new_username

        if new_email:
            user.email = new_email

        db.session.commit()
        return jsonify(user.to_dict()), 200

    except Exception as e:
        print(" Profile update error:", str(e))
        return jsonify({"message": "Internal server error"}), 500


@auth_bp.route("/api/profile/image", methods=["POST"])
@jwt_required()
def upload_profile_image():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        image = request.files.get("image")
        if not image:
            return jsonify({"message": "No image uploaded"}), 400

        filename = secure_filename(image.filename)
        profile_dir = os.path.join("static", "profile")
        os.makedirs(profile_dir, exist_ok=True)
        image.save(os.path.join(profile_dir, filename))

        user.profile_image = filename
        db.session.commit()

        return jsonify({
            "message": "Profile image updated",
            "profile_image_url": f"{request.host_url.rstrip('/')}/static/profile/{filename}"
        }), 200

    except Exception as e:
        print("🚨 Profile image upload error:", str(e))
        return jsonify({"message": "Internal server error"}), 500