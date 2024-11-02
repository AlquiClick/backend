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
from schemas import UserSchema, MinimalUserSchema, PropertySchema

default_bp = Blueprint('default', __name__)

@default_bp.route("/properties", methods=['POST', 'GET', 'PUT', 'DELETE'])
# @jwt_required()
def properties():
    if request.method == 'POST':
        return {}
    if request.method == 'GET':
        mock_property = [
            {
                "id": 1,
                "title": "Lujoso apartamento en el centro",
                "description": "Moderno apartamento en el centro de la ciudad, cerca de todas las comodidades y transporte público.",
                "price": 1200.50,
                "address": "Calle Principal 123",
                "city": "Madrid",
                "state": "Madrid",
                "country": "España",
                "available": True,
                "bedrooms": 2,
                "bathrooms": 1,
                "square_feet": 800,
                "property_type": "apartment",
                "created_at": "2023-10-01T12:00:00",
                "updated_at": "2023-10-01T12:00:00"
            },
            {
                "id": 2,
                "title": "Casa de campo con vistas al mar",
                "description": "Hermosa casa de campo situada en la costa, con vistas al mar y jardín privado.",
                "price": 2500.75,
                "address": "Camino a la Playa s/n",
                "city": "Málaga",
                "state": "Andalucía",
                "country": "España",
                "available": False,
                "bedrooms": 4,
                "bathrooms": 3,
                "square_feet": 1500,
                "property_type": "house",
                "created_at": "2023-08-15T08:30:00",
                "updated_at": "2023-08-16T09:15:00"
            },
            {
                "id": 3,
                "title": "Condominio moderno en zona tranquila",
                "description": "Condominio de reciente construcción en zona residencial tranquila, ideal para familias.",
                "price": 1800.00,
                "address": "Av. Las Flores 456",
                "city": "Barcelona",
                "state": "Cataluña",
                "country": "España",
                "available": True,
                "bedrooms": 3,
                "bathrooms": 2,
                "square_feet": 1100,
                "property_type": "condo",
                "created_at": "2023-09-10T14:45:00",
                "updated_at": "2023-09-11T11:00:00"
            },
            {
                "id": 4,
                "title": "Penthouse en la Gran Manzana",
                "description": "Exclusivo penthouse en el centro de Nueva York, con vistas impresionantes y acabados de lujo.",
                "price": 7500.90,
                "address": "5th Avenue 789",
                "city": "New York",
                "state": "New York",
                "country": "Estados Unidos",
                "available": False,
                "bedrooms": 5,
                "bathrooms": 4,
                "square_feet": 3000,
                "property_type": "penthouse",
                "created_at": "2023-07-22T10:20:00",
                "updated_at": "2023-07-25T15:10:00"
            },
            {
                "id": 5,
                "title": "Estudio en el corazón de Tokio",
                "description": "Compacto y funcional estudio en Tokio, ideal para estudiantes o jóvenes profesionales.",
                "price": 950.30,
                "address": "Shibuya 109",
                "city": "Tokio",
                "state": "Kanto",
                "country": "Japón",
                "available": True,
                "bedrooms": 1,
                "bathrooms": 1,
                "square_feet": 350,
                "property_type": "studio",
                "created_at": "2023-06-01T18:00:00",
                "updated_at": "2023-06-02T10:30:00"
            }
        ];
        
        return jsonify(mock_property), 201
    if request.method == 'PUT':
        return
    if request.method == 'DELETE':
        return