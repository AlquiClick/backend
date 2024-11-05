from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt, jwt_required
from werkzeug.security import generate_password_hash
from app import db
from models import User
from schemas import UserSchema, MinimalUserSchema

user_bp = Blueprint('user', __name__)

@user_bp.route("/users", methods=['GET'])
@jwt_required()
def get_users():
    """
    Retrieve a list of all users
    ---
    security:
      - Bearer: []
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: "JWT Token with 'Bearer ' prefix"
    responses:
      200:
        description: List of users
        schema:
          type: array
          items:
            oneOf:
              - type: object
                properties:
                  id:
                    type: integer
                    description: The ID of the user
                  username:
                    type: string
                    description: The username of the user
                  email:
                    type: string
                    description: The email of the user
                  is_active:
                    type: boolean
                    description: The status of the user
              - type: object
                properties:
                  username:
                    type: string
                    description: The username of the user
    """
    additional_data = get_jwt()
    admin = additional_data.get('is_admin')
    users = User.query.all()

    if admin:
        return UserSchema().dump(users, many=True)
    return MinimalUserSchema().dump(users, many=True)


@user_bp.route("/users", methods=['POST'])
@jwt_required()
def create_user():
    """
    Create a new user (Admin only)
    ---
    security:
      - Bearer: []
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: "JWT Token with 'Bearer ' prefix"
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: The username for the new user
            email:
              type: string
              description: The email address for the new user
            password:
              type: string
              description: The password for the new user
          required:
            - username
            - email
            - password
    responses:
      201:
        description: User created successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User {username} is created"
      403:
        description: Unauthorized action (if not admin)
        schema:
          type: object
          properties:
            message:
              type: string
              example: "No tienes permisos para crear propiedades"
      404:
        description: Error occurred while creating user
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Algo malio sal"
    """
    additional_data = get_jwt()
    admin = additional_data.get('is_admin')

    if not admin:
        return jsonify({
            "message": "No tienes permisos para crear usuarios"
        }), 403

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
            is_active=True
        )

        db.session.add(nuevo_user)
        db.session.commit()

        return jsonify({
            "message": f'User {username} is created',
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "Algo malio sal",
            "error": str(e)
        }), 404
