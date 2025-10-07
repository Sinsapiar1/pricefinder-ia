import os

# Solo cargar dotenv si existe el archivo .env (no en producción)
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

class Config:
    """Configuración base de la aplicación"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configuración de APIs (estas se recibirán del frontend)
    GEMINI_API_KEY = None
    SCRAPER_API_KEY = None
    
    # Configuración de la aplicación
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Configuración de producción
    TESTING = os.environ.get('TESTING', 'False').lower() == 'true'
    
    # Sitios para scraping - Estrategia Híbrida (Gratis + Premium)
    # Gratis: Amazon + eBay (funcionan con plan gratuito)
    # Premium: Walmart + BestBuy (requieren ScraperAPI pago)
    TARGET_SITES = [
        'amazon.com',      # ✅ GRATIS - Funciona siempre
        'ebay.com',        # ✅ GRATIS - Funciona generalmente
        'walmart.com',     # 💎 PREMIUM - Requiere plan pago
        'bestbuy.com',     # 💎 PREMIUM - Requiere plan pago
    ]
    
    # Clasificación de tiendas
    FREE_TIER_SITES = ['amazon.com', 'ebay.com']
    PREMIUM_SITES = ['walmart.com', 'bestbuy.com']
    
    # Límites optimizados
    MAX_RESULTS_PER_SITE = 5
    REQUEST_TIMEOUT = 25

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    TESTING = False
    
class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    
class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    DEBUG = True