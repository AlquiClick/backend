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
from models import User, Contract, Property
from schemas import ContractSchema

contract_bp = Blueprint('contract', __name__)

@contract_bp.route("/contract", methods=['POST', 'GET'])
@jwt_required()
def contract():
    additional_data = get_jwt()
    admin = additional_data.get('is_admin')

    if request.method == 'POST':
        if not admin:
            return jsonify({
                "message": "No tienes permisos para crear contratos"
            }), 403

        data = request.get_json()
        property_id = data.get('property_id')
        renter_id = data.get('renter_id')
        owner_id = data.get('owner_id')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        monthly_rent = data.get('monthly_rent')
        status = data.get('status', True)

        if not all([property_id, renter_id, owner_id, start_date, end_date, monthly_rent]):
            return jsonify({"message": "Todos los campos son obligatorios"}), 400

        try:
            renter = User.query.get(renter_id)
            owner = User.query.get(owner_id)
            property = Property.query.get(property_id)
            if not renter or not owner or not property:
                return jsonify({"message": "Propiedad, propietario o inquilino no encontrados"}), 404

            new_contract = Contract(
                property_id=property_id,
                renter_id=renter_id,
                owner_id=owner_id,
                start_date=start_date,
                end_date=end_date,
                monthly_rent=monthly_rent,
                status=status
            )

            db.session.add(new_contract)
            db.session.commit()

            return jsonify({
                "message": f"Contract created successfully",
                "contract": ContractSchema().dump(new_contract)
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "message": "Error al crear el contrato",
                "error": str(e)
            }), 500

    contracts = Contract.query.all()
    return ContractSchema().dump(contracts, many=True)