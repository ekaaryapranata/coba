from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db
from ..models.auth import UserModel

profile = Blueprint('profile', __name__)


@profile.route('/reset', methods=['POST'])
def reset():
    if request.content_type != 'application/json':
        return jsonify({"error": True, "message": "Content-Type must be application/json"}), 415

    data = request.get_json()
    if not data:
        return jsonify({"error": True, "message": "Please Change JSON file"}), 400

    email = data.get('UserEmail')
    current_password = data.get('UserPass')
    new_name = data.get('new_name')
    new_password = data.get('new_password')

    if not email or not current_password or not new_name or not new_password:
        return jsonify({"error": True, "message": "Email, current password, new name, and new password are required"}), 400

    if len(new_password) < 8:
        return jsonify({"error": True, "message": "New password must be at least 8 characters long"}), 400

    user = UserModel.query.filter_by(UserEmail=email).first()

    if not user or not check_password_hash(user.password, current_password):
        return jsonify({"error": True, "message": "Please input the appropriate email and password data "}), 401

    user.name = new_name
    user.password = generate_password_hash(new_password, method='pbkdf2:sha256')

    try:
        db.session.commit()
        return jsonify({"error": False, "message": "User details updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": True, "message": str(e)}), 500