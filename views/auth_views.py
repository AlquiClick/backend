from flask import Blueprint, request, jsonify
from datetime import timedelta
from flask_jwt_extended import (
    get_jwt,
    jwt_required,
    create_access_token,
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from app import db
from models import User
from schemas import UserSchema, MinimalUserSchema

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/users", methods=['POST', 'GET'])
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
    
@auth_bp.route("/login", methods=['POST'])
def login():
    data = request.authorization
    username = data.username
    password = data.password

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(pwhash=user.password, password=password):
        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(minutes=10),
            additional_claims=dict(
                is_admin=user.is_admin,
            )
        ) 
        return jsonify({
            "message": f'Login exitoso {username}',
            "token": f'{access_token}',
        }), 201
    else:
         return jsonify({
            "message": 'Algo malio sal',
        }), 404
    
@auth_bp.route("/register", methods=['POST'])
def register():

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
            is_admin=True,
            is_active=True
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