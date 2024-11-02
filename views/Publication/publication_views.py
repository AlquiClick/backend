from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    get_jwt,
    jwt_required,
)
from app import db
from models import Publication, Property, Image, User
from schemas import PublicationSchema

publication_bp = Blueprint('publication', __name__)

@publication_bp.route("/publications", methods=['POST', 'GET'])
@jwt_required()
def publications():
    additional_data = get_jwt()
    admin = additional_data.get('is_admin')

    if request.method == 'POST':
        if not admin:
            return jsonify({
                "message": "No tienes permisos para crear publicaciones"
            }), 403

        data = request.get_json()
        property_id = data.get('property_id')
        image_id = data.get('image_id')
        user_id = data.get('user_id')
        title = data.get('title')
        description = data.get('description')
        price_shown = data.get('price_shown')
        publication_status_id = data.get('publication_status_id')
        publish_date = data.get('publish_date')
        expiry_date = data.get('expiry_date')
        status = data.get('status', 'active')

        try:
            new_publication = Publication(
                property_id=property_id,
                image_id=image_id,
                user_id=user_id,
                title=title,
                description=description,
                price_shown=price_shown,
                publication_status_id=publication_status_id,
                publish_date=publish_date,
                expiry_date=expiry_date,
                status=status
            )

            db.session.add(new_publication)
            db.session.commit()

            return jsonify({
                "message": f"Publication '{title}' created successfully",
                "publication": PublicationSchema().dump(new_publication)
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "message": "Error al crear la publicación",
                "error": str(e)
            }), 500

    publications = Publication.query.all()
    return PublicationSchema().dump(publications, many=True)
