from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    get_jwt,
    jwt_required,
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from app import db
from models import User
from schemas import UserSchema, MinimalUserSchema

user_bp = Blueprint('user', __name__)

@user_bp.route("/users", methods=['POST', 'GET'])
@jwt_required()
def user():
    additional_data = get_jwt()
    admin = additional_data.get('is_admin')

    if request.method == 'POST':
        if admin:
            data = request.get_json()
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            passwordHash = generate_password_hash(
                password=password,
                method='pbkdf2',
                salt_length=8
            )
            try:
                nuevo_user = User(
                    username=username,
                    email=email,
                    password=passwordHash,
                    is_active=1
                )

                db.session.add(nuevo_user)
                db.session.commit()

                return jsonify({
                    "message": f'User {username} is created',
                }), 201
            except:
                return jsonify({
                    "message": 'Algo malio sal',
                }), 404

    users = User.query.all()

    if admin:
        return UserSchema().dump(users, many=True)
    return MinimalUserSchema().dump(users, many=True)
