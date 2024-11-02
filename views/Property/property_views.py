from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    get_jwt,
    jwt_required,
)
from app import db
from models import Property
from schemas import PropertySchema  # Asumimos que tienes un esquema para serializar Property

property_bp = Blueprint('property', __name__)

@property_bp.route("/property", methods=['POST', 'GET'])
@jwt_required()
def property():
    additional_data = get_jwt()
    admin = additional_data.get('is_admin')

    if request.method == 'POST':
        if not admin:
            return jsonify({
                "message": "No tienes permisos para crear propiedades"
            }), 403

        data = request.get_json()
        address = data.get('address')
        rooms = data.get('rooms')
        bathrooms = data.get('bathrooms')
        garage_capacity = data.get('garage_capacity')
        year_built = data.get('year_built')
        property_status_id = data.get('property_status_id')
        monthly_rent = data.get('monthly_rent')
        owner_id = data.get('owner_id')
        active = data.get('active', True)

        try:
            new_property = Property(
                address=address,
                rooms=rooms,
                bathrooms=bathrooms,
                garage_capacity=garage_capacity,
                year_built=year_built,
                property_status_id=property_status_id,
                monthly_rent=monthly_rent,
                owner_id=owner_id,
                active=active
            )

            db.session.add(new_property)
            db.session.commit()

            return jsonify({
                "message": f"Property at {address} created successfully",
                "property": PropertySchema().dump(new_property)
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "message": "Error al crear la propiedad",
                "error": str(e)
            }), 500

    properties = Property.query.all()
    return PropertySchema().dump(properties, many=True)
