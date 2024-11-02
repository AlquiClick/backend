from app import ma
from models import User
from marshmallow import fields

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    password = ma.auto_field()
    is_admin = ma.auto_field()

class MinimalUserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    username = ma.auto_field()

class PropertySchema(ma.Schema):
    # class Meta:
    #     model = Property
    #     load_instance = True

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    price = fields.Float(required=True)
    address = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=True)
    country = fields.Str(required=True)
    available = fields.Bool()
    bedrooms = fields.Int(required=True)
    bathrooms = fields.Int(required=True)
    square_feet = fields.Int()
    property_type = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
