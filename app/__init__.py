from flask import Flask
from flask_cors import CORS
from config import Config
import os

def create_app(config_class=Config):
    """Factory para crear la aplicación Flask - Optimizado para Vercel"""
    
    # Determinar el directorio base
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    # Paths absolutos
    template_folder = os.path.join(base_dir, 'templates')
    static_folder = os.path.join(base_dir, 'static')
    
    # Crear app Flask
    app = Flask(__name__, 
                template_folder=template_folder,
                static_folder=static_folder,
                static_url_path='/static')
    
    app.config.from_object(config_class)
    
    # CORS configurado para permitir todos los orígenes (necesario en Vercel)
    CORS(app, 
         resources={r"/*": {"origins": "*"}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "OPTIONS"])
    
    # Registrar blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Log de rutas (solo en debug)
    if os.environ.get('FLASK_ENV') != 'production':
        print("\n=== RUTAS REGISTRADAS ===")
        for rule in app.url_map.iter_rules():
            methods = ','.join(rule.methods - {'HEAD', 'OPTIONS'})
            print(f"  [{methods:7}] {rule.rule} -> {rule.endpoint}")
        print("=" * 30 + "\n")
    
    return app