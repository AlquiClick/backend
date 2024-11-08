from app import ma
from models import User, Property, Publication, Image
from marshmallow import fields

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    password = ma.auto_field()
    email = ma.auto_field()
    is_admin = ma.auto_field()

class MinimalUserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    username = ma.auto_field()

class PropertySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Property
        load_instance = True

    id = fields.Int(dump_only=True)
    address = fields.Str(required=True)
    rooms = fields.Int(required=True)
    bathrooms = fields.Int(required=True)
    garage_capacity = fields.Int()
    year_built = fields.Int()
    property_status_id = fields.Int()
    monthly_rent = fields.Decimal(as_string=True)
    owner_id = fields.Int(required=True)
    active = fields.Bool()

class ImageSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Image
        load_instance = True

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    url = fields.Str(required=True)

class PublicationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Publication
        load_instance = True

    id = fields.Int(dump_only=True)
    property_id = fields.Int()
    image_id = fields.Int()
    user_id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    price_shown = fields.Decimal(as_string=True)
    publication_status_id = fields.Int()
    publish_date = fields.Date()
    expiry_date = fields.Date()
    status = fields.Str()

    # Campos relacionados
    property = fields.Nested(PropertySchema)
    image = fields.Nested(ImageSchema)

class MinimalPublicationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Publication

    id = fields.Int(dump_only=True)
    property_id = fields.Int()
    image_id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    publish_date = fields.Date()

    # Campos relacionados
    property = fields.Nested(PropertySchema)
    image = fields.Nested(ImageSchema)

class ContractSchema(ma.SQLAlchemySchema):
    id = fields.Int(dump_only=True)
    property_id = fields.Int(required=True)
    renter_id = fields.Int(required=True)
    owner_id = fields.Int(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    monthly_rent = fields.Decimal(as_string=True)
    status = fields.Boolean()
