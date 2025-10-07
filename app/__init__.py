from flask import Flask
from flask_cors import CORS
from config import Config

def create_app(config_class=Config):
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Habilitar CORS para Vercel
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Registrar blueprints/rutas
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Debug: Imprimir rutas registradas
    print("Rutas registradas:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} -> {rule.endpoint}")
    
    return app