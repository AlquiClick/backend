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
from models import User, Person
from schemas import UserSchema, MinimalUserSchema

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/users", methods=['POST', 'GET'])
@jwt_required()
def user():
    """
    List users or create user
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
    get:
      description: List all users
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
                    username:
                      type: string
                    is_admin:
                      type: boolean
                    password:
                      type: string
                - type: object
                  properties:
                    username:
                      type: string
    post:
      description: Create a new user
      responses:
        201:
          description: User created
          schema:
            type: object
            properties:
              message:
                type: string
                example: "User {username} is created"
        403:
          description: Unauthorized
          schema:
            type: object
            properties:
              message:
                type: string
                example: "Unauthorized access"
    """
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
    """
    User login
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: |
          Basic authorization header. Format: 'Basic {base64(username:password)}'.
          To encode the credentials, you can use the following command:
          ```
          echo -n "username:password" | base64
          ```
          Example:
          ```
          echo -n "nuevo_usuario:password123" | base64
          ```
    responses:
      201:
        description: Login successful
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Login exitoso nuevo_usuario"
            token:
              type: string
              example: "JWT token string"
      404:
        description: Invalid credentials
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Algo malio sal"
    """
    data = request.authorization
    username = data.username
    password = data.password

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(pwhash=user.password, password=password):
        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(minutes=100000),
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
    """
    Register a new user
    ---
    parameters:
      - name: body
        in: body
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
        description: User successfully created
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User {username} is created"
      404:
        description: Error occurred while creating user
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Algo malio sal"
    """
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    date_of_birth = data.get('date_of_birth')

    passwordHash = generate_password_hash(
        password=password,
        method='pbkdf2',
        salt_length=8
    )

    try:
        nueva_persona = Person(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth
        )

        db.session.add(nueva_persona)
        db.session.flush()

        nuevo_user = User(
            username=username,
            email=email,
            password=passwordHash,
            is_admin=True,
            is_active=True,
            person_id=nueva_persona.id
        )

        db.session.add(nuevo_user)
        db.session.commit()

        return jsonify({
            "message": f'User {username} is created with Person {first_name} {last_name}',
        }), 201
    except Exception as e:
        db.session.rollback()  # Revierte en caso de error
        return jsonify({
            "message": 'Algo malio sal',
            "error": str(e)
        }), 400