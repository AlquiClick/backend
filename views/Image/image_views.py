from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    get_jwt,
    jwt_required,
)
from app import db
from models import Image
from schemas import ImageSchema

image_bp = Blueprint('image', __name__)

@image_bp.route("/image", methods=['POST', 'GET'])
@jwt_required()
def image():
    additional_data = get_jwt()
    admin = additional_data.get('is_admin')

    if request.method == 'POST':
        if not admin:
            return jsonify({
                "message": "No tienes permisos para crear propiedades"
            }), 403

        data = request.get_json()
        name = data.get('name')
        url = data.get('url')

        try:
            new_image = Image(
                name=name,
                url=url
            )

            db.session.add(new_image)
            db.session.commit()

            return jsonify({
                "message": f"Image created successfully",
                "image": ImageSchema().dump(new_image)
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "message": "Error al crear la imagen",
                "error": str(e)
            }), 500

    images = Image.query.all()
    return ImageSchema().dump(images, many=True)
