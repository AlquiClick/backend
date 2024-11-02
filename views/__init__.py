from .auth_views import auth_bp
from .Users.user_views import user_bp
from .default_views import default_bp

def register_bp(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(default_bp)
