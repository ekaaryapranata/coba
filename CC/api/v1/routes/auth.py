from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
import jwt
import datetime
from extensions import db
from ..models.auth import UserModel

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    if request.content_type != 'application/json':
        return jsonify({"error": True, "message": "Content-Type must be application/json"}), 415

    data = request.get_json()
    if not data:
        return jsonify({"error": True, "message": "Please Change JSON file"}), 400

    name = data.get('UserName')
    email = data.get('UserEmail')
    password = data.get('UserPass')

    if not name or not email or not password:
        return jsonify({"error": True, "message": "Please input name,email,passwod"}), 400

    if len(password) < 8:
        return jsonify({"error": True, "message": "Please input 8 char or long in pass column"}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    new_user = UserModel(UserName=name, UserEmail=email, UserPass=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"error": False, "message": "yee , Register success now u can login "}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": True, "message": "Email useed, please use new email for register"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": True, "message": str(e)}), 500

@auth.route('/login', methods=['POST'])
def login():
    if request.content_type != 'application/json':
        return jsonify({"error": True, "message": "Content-Type must be application/json"}), 415

    data = request.get_json()
    if not data:
        return jsonify({"error": True, "message": "Please Change JSON file"}), 400

    email = data.get('UserEmail')
    password = data.get('UserPass')

    user = UserModel.query.filter_by(UserEmail=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": True, "message": "Please check again email & password "}), 401

    token = jwt.encode({
        'userId': f'user-{user.id}',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }, 'your_secret_key_here', algorithm='HS256')

    return jsonify({
        "error": False,
        "message": "success",
        "loginResult": {
            "userId": f'user-{user.id}',
            "name": user.name,
            "token": token
        }
    }), 200
