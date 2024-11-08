from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt, jwt_required
from app import db
from models import Property
from schemas import PropertySchema

property_bp = Blueprint('property', __name__)

@property_bp.route("/property", methods=['GET'])
@jwt_required()
def get_properties():
    """
    Retrieve a list of all properties
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
        description: List of properties
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: The ID of the property
              address:
                type: string
                description: The address of the property
              rooms:
                type: integer
                description: Number of rooms
              bathrooms:
                type: integer
                description: Number of bathrooms
              garage_capacity:
                type: integer
                description: Garage capacity
              year_built:
                type: integer
                description: Year the property was built
              property_status_id:
                type: integer
                description: Status ID of the property
              monthly_rent:
                type: number
                description: Monthly rent for the property
              owner_id:
                type: integer
                description: ID of the property owner
              active:
                type: boolean
                description: Whether the property is active
    """
    properties = Property.query.all()
    return PropertySchema().dump(properties, many=True)


@property_bp.route("/property", methods=['POST'])
@jwt_required()
def create_property():
    """
    Create a new property (Admin only)
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
            address:
              type: string
              description: The address of the property
            rooms:
              type: integer
              description: Number of rooms in the property
            bathrooms:
              type: integer
              description: Number of bathrooms in the property
            garage_capacity:
              type: integer
              description: Garage capacity
            year_built:
              type: integer
              description: Year the property was built
            property_status_id:
              type: integer
              description: Status ID of the property
            monthly_rent:
              type: number
              description: Monthly rent for the property
            owner_id:
              type: integer
              description: ID of the property owner
            active:
              type: boolean
              description: Whether the property is active
          required:
            - address
            - rooms
            - bathrooms
            - garage_capacity
            - year_built
            - property_status_id
            - monthly_rent
            - owner_id
    responses:
      201:
        description: Property created successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Property at {address} created successfully"
            property:
              type: object
              properties:
                id:
                  type: integer
                  description: The ID of the property
                address:
                  type: string
                  description: The address of the property
                rooms:
                  type: integer
                  description: Number of rooms
                bathrooms:
                  type: integer
                  description: Number of bathrooms
                garage_capacity:
                  type: integer
                  description: Garage capacity
                year_built:
                  type: integer
                  description: Year the property was built
                property_status_id:
                  type: integer
                  description: Status ID of the property
                monthly_rent:
                  type: number
                  description: Monthly rent for the property
                owner_id:
                  type: integer
                  description: ID of the property owner
                active:
                  type: boolean
                  description: Whether the property is active
      403:
        description: Unauthorized action (if not admin)
        schema:
          type: object
          properties:
            message:
              type: string
              example: "No tienes permisos para crear propiedades"
      500:
        description: Server error during property creation
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Error al crear la propiedad"
            error:
              type: string
              description: Detailed error message
    """
    additional_data = get_jwt()
    admin = additional_data.get('is_admin')

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
    # owner_id = data.get('owner_id')
    owner_id = 1
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

@property_bp.route("/property", methods=['DELETE'])
@jwt_required()
def inactive_property():
    """
    Inactive a specified property (Admin only)
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
            property_id:
              type: integer
              description: The ID of the property that becomes inactive
          required:
            - property_id
    responses:
      201:
        description: Property inactive successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Propiedad eliminada exitosamente"
      403:
        description: Property not found
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Propiedad no encontrada"
      500:
        description: Server error during property deleted
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Error al eliminar la propiedad"
            error:
              type: string
              description: Detailed error message
    """
    additional_data = get_jwt()
    admin = additional_data.get('is_admin')

    if not admin:
        return jsonify({
            "message": "No tienes permisos para eliminar propiedades"
        }), 403

    data = request.get_json()
    property_id = data.get('property_id')

    propery = Property.query.filter_by(id=property_id).first()

    if not propery:
      return jsonify({
          "message": "Propiedad no encontrada"
      }), 404

    propery.active = 0
    db.session.add(propery)
    try:
        db.session.commit()
        return jsonify({"message": "Propiedad eliminada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error al eliminar la propiedad", "error": str(e)}), 500

@property_bp.route("/property", methods=['PUT'])
@jwt_required()
def update_property():
    """
    Actualiza una propiedad existente (solo para administradores)
    ---
    security:
      - Bearer: []
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: "Token JWT con el prefijo 'Bearer '"
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            property_id:
              type: integer
              description: ID de la propiedad a actualizar
            address:
              type: string
              description: Nueva dirección de la propiedad
            rooms:
              type: integer
              description: Número de habitaciones
            bathrooms:
              type: integer
              description: Número de baños
            garage_capacity:
              type: integer
              description: Capacidad del garaje
            year_built:
              type: integer
              description: Año de construcción
            property_status_id:
              type: integer
              description: ID del estado de la propiedad
            monthly_rent:
              type: number
              description: Alquiler mensual
            owner_id:
              type: integer
              description: ID del propietario
            active:
              type: boolean
              description: Estado de actividad de la propiedad
          required:
            - property_id
    responses:
      200:
        description: Propiedad actualizada exitosamente
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Propiedad actualizada exitosamente"
            property:
              type: object
              properties:
                id:
                  type: integer
                address:
                  type: string
                rooms:
                  type: integer
                bathrooms:
                  type: integer
                garage_capacity:
                  type: integer
                year_built:
                  type: integer
                property_status_id:
                  type: integer
                monthly_rent:
                  type: number
                owner_id:
                  type: integer
                active:
                  type: boolean
      403:
        description: Acción no autorizada (si no es administrador)
        schema:
          type: object
          properties:
            message:
              type: string
              example: "No tienes permisos para actualizar propiedades"
      404:
        description: Propiedad no encontrada
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Propiedad no encontrada"
      500:
        description: Error del servidor durante la actualización de la propiedad
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Error al actualizar la propiedad"
            error:
              type: string
              description: Mensaje detallado del error
    """
    additional_data = get_jwt()
    admin = additional_data.get('is_admin')

    if not admin:
        return jsonify({
            "message": "No tienes permisos para actualizar propiedades"
        }), 403

    data = request.get_json()
    property_id = data.get('property_id')

    if not property_id:
        return jsonify({
            "message": "El 'property_id' es obligatorio"
        }), 400

    property = Property.query.filter_by(id=property_id).first()

    if not property:
        return jsonify({
            "message": "Propiedad no encontrada"
        }), 404

    for key, value in data.items():
        if key != 'property_id' and hasattr(property, key):
            setattr(property, key, value)

    try:
        db.session.commit()
        return jsonify({
            "message": "Propiedad actualizada exitosamente",
            "property": PropertySchema().dump(property)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "Error al actualizar la propiedad",
            "error": str(e)
        }), 500