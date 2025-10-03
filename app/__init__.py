from flask import Flask
from flask_cors import CORS
from config import Config

def create_app(config_class=Config):
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Habilitar CORS para permitir peticiones desde el frontend
    CORS(app)
    
    # Registrar blueprints/rutas
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app