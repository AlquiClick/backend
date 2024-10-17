from .auth_views import auth_bp
from .shop.shop_views import shop_bp

def register_bp(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(shop_bp)