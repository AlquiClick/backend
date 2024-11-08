from .auth_views import auth_bp
from .Users.user_views import user_bp
from .Property.property_views import property_bp
from .Publication.publication_views import publication_bp
from .Image.image_views import image_bp
from .Contract.contract_views import contract_bp

def register_bp(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(property_bp)
    app.register_blueprint(publication_bp)
    app.register_blueprint(image_bp)
    app.register_blueprint(contract_bp)
