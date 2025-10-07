from flask import Flask
from flask_cors import CORS
from config import Config

def create_app(config_class=Config):
    """Factory para crear la aplicación Flask"""
    import os
    # Configurar paths absolutos para templates y static
    template_folder = os.path.join(os.path.dirname(__file__), 'templates')
    static_folder = os.path.join(os.path.dirname(__file__), 'static')
    
    app = Flask(__name__, 
                template_folder=template_folder,
                static_folder=static_folder,
                static_url_path='/static')
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