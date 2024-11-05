from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt, jwt_required
from app import db
from models import Image
from schemas import ImageSchema

image_bp = Blueprint('image', __name__)

@image_bp.route("/image", methods=['GET'])
@jwt_required()
def get_images():
    """
    Retrieve a list of all images
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
        description: List of images
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: The ID of the image
              name:
                type: string
                description: The name of the image
              url:
                type: string
                description: The URL of the image
    """
    images = Image.query.all()
    return ImageSchema().dump(images, many=True)

@image_bp.route("/image", methods=['POST'])
@jwt_required()
def create_image():
    """
    Create a new image (Admin only)
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
            name:
              type: string
              description: The name of the image
            url:
              type: string
              description: The URL of the image
          required:
            - name
            - url
    responses:
      201:
        description: Image created successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Image created successfully"
            image:
              type: object
              properties:
                id:
                  type: integer
                  description: The ID of the image
                name:
                  type: string
                  description: The name of the image
                url:
                  type: string
                  description: The URL of the image
      403:
        description: Unauthorized action (if not admin)
        schema:
          type: object
          properties:
            message:
              type: string
              example: "No tienes permisos para crear propiedades"
      500:
        description: Server error during image creation
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Error al crear la imagen"
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

@image_bp.route("/image", methods=['PUT'])
@jwt_required()
def delete_image():
    """
    Delete a specific image (Admin only)
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
            image_id:
              type: string
              description: The ID of image that becomes inactive
          required:
            - image_id
    responses:
      201:
        description: Image deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Imagen eliminida correctamente"
      403:
        description: Unauthorized action (if not admin)
        schema:
          type: object
          properties:
            message:
              type: string
              example: "No tienes permisos para eliminar imagenes"
      404:
        description: Image not found
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Imagen no encontrada"
      500:
        description: Server error during image creation
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Error al crear la imagen"
            error:
              type: string
              description: Detailed error message
    """
    additional_data = get_jwt()
    admin = additional_data.get('is_admin')

    if not admin:
        return jsonify({
            "message": "No tienes permisos para eliminar imagenes"
        }), 403

    data = request.get_json()
    image_id = data.get('image_id')

    try:
        image = Image().query.filter_by(id=image_id).first()

        if not image:
          return jsonify({
              "message": "Imagen no encontrada"
          }), 404

        db.session.delete(image)
        db.session.commit()

        return jsonify({
            "message": f"Imagen eliminida correctamente"
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "Error al eliminar la imagen",
            "error": str(e)
        }), 500
