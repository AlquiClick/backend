from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity
from app import db
from models import Publication
from schemas import PublicationSchema, MinimalPublicationSchema

publication_bp = Blueprint('publication', __name__)

@publication_bp.route("/publications", methods=['GET'])
@jwt_required(optional=True)
def get_publications():
    """
    Retrieve a list of all publications
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
        description: List of publications
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: The ID of the publication
              property_id:
                type: integer
                description: ID of the associated property
              image_id:
                type: integer
                description: ID of the associated image
              user_id:
                type: integer
                description: ID of the user who created the publication
              title:
                type: string
                description: The title of the publication
              description:
                type: string
                description: The description of the publication
              price_shown:
                type: number
                description: The price shown for the publication
              publication_status_id:
                type: integer
                description: Status ID of the publication
              publish_date:
                type: string
                format: date
                description: The date when the publication was created
              expiry_date:
                type: string
                format: date
                description: The expiration date of the publication
              status:
                type: string
                description: The status of the publication (e.g., 'active')
    """

    user_id = get_jwt_identity()
    active_publications = db.session.query(Publication).filter_by(status='active').join(Publication.property).join(Publication.image).all()

    if user_id:
      return PublicationSchema().dump(active_publications, many=True), 200
    else:
      return MinimalPublicationSchema().dump(active_publications, many=True), 200



@publication_bp.route("/publications", methods=['POST'])
@jwt_required()
def create_publication():
    """
    Create a new publication (Admin only)
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
              description: The ID of the property for this publication
            image_id:
              type: integer
              description: The ID of the image for this publication
            user_id:
              type: integer
              description: The ID of the user creating the publication
            title:
              type: string
              description: The title of the publication
            description:
              type: string
              description: The description of the publication
            price_shown:
              type: number
              description: The price displayed in the publication
            publication_status_id:
              type: integer
              description: The status ID of the publication
            publish_date:
              type: string
              format: date
              description: The date when the publication goes live (format YYYY-MM-DD)
            expiry_date:
              type: string
              format: date
              description: The expiration date of the publication (format YYYY-MM-DD)
            status:
              type: string
              description: The status of the publication (e.g., 'active')
          required:
            - property_id
            - user_id
            - title
            - description
            - price_shown
            - publication_status_id
            - publish_date
            - expiry_date
    responses:
      201:
        description: Publication created successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Publication '{title}' created successfully"
            publication:
              type: object
              properties:
                id:
                  type: integer
                  description: The ID of the publication
                title:
                  type: string
                  description: The title of the publication
                description:
                  type: string
                  description: The description of the publication
                price_shown:
                  type: number
                  description: The price shown for the publication
                publish_date:
                  type: string
                  format: date
                  description: The publication's start date
                expiry_date:
                  type: string
                  format: date
                  description: The publication's end date
                status:
                  type: string
                  description: The status of the publication
      403:
        description: Unauthorized action (if not admin)
        schema:
          type: object
          properties:
            message:
              type: string
              example: "No tienes permisos para crear publicaciones"
      500:
        description: Server error during publication creation
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Error al crear la publicación"
            error:
              type: string
              description: Detailed error message
    """
    additional_data = get_jwt()
    admin = additional_data.get('is_admin')

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

@publication_bp.route("/publications", methods=['PUT'])
@jwt_required()
def inactive_publication():
    """
    Inactive a specified publication (Admin only)
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
            publication_id:
              type: integer
              description: The ID of the publication that becomes inactive
          required:
            - publication_id
    responses:
      201:
        description: Publication inactive successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Publicación eliminada exitosamente"
      403:
        description: Publication not found
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Publicación no encontrada"
      500:
        description: Server error during publication creation
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Error al eliminar la publicación"
            error:
              type: string
              description: Detailed error message
    """
    additional_data = get_jwt()
    admin = additional_data.get('is_admin')

    if not admin:
        return jsonify({
            "message": "No tienes permisos para crear publicaciones"
        }), 403

    data = request.get_json()
    publication_id = data.get('publication_id')

    publication = Publication.query.filter_by(id=publication_id).first()

    if not publication:
      return jsonify({
          "message": "Publicación no encontrada"
      }), 404

    publication.status = 'inactive'

    try:
        db.session.commit()
        return jsonify({"message": "Publicación eliminada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error al eliminar la publicación", "error": str(e)}), 500
