from flask import Blueprint, render_template, request, jsonify
from app.services.scraper import ProductScraper
from app.services.gemini_analyzer import GeminiAnalyzer
import traceback

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Renderiza la página principal"""
    return render_template('index.html')

@main_bp.route('/api/search', methods=['POST'])
def search_products():
    """Endpoint principal para buscar productos"""
    try:
        print("\n" + "="*50)
        print("🚀 Nueva búsqueda iniciada")
        print("="*50)
        
        # Obtener datos del request
        data = request.get_json()
        
        # Validar campos requeridos
        gemini_key = data.get('gemini_api_key', '').strip()
        scraper_key = data.get('scraper_api_key', '').strip()
        product_name = data.get('product_name', '').strip()
        
        print(f"📦 Producto solicitado: {product_name}")
        print(f"🔑 Gemini Key: {'✓' if gemini_key else '✗'}")
        print(f"🔑 Scraper Key: {'✓' if scraper_key else '✗'}")
        
        if not all([gemini_key, scraper_key, product_name]):
            return jsonify({
                'success': False,
                'error': 'Todos los campos son requeridos: Gemini API Key, Scraper API Key y Nombre del Producto'
            }), 400
        
        # Inicializar servicios
        print("\n📡 Inicializando servicios...")
        try:
            scraper = ProductScraper(scraper_key)
            print("  ✓ Scraper inicializado")
        except Exception as e:
            print(f"  ✗ Error al inicializar scraper: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Error al inicializar el servicio de scraping: {str(e)}'
            }), 500
        
        try:
            analyzer = GeminiAnalyzer(gemini_key)
            print("  ✓ Analyzer inicializado")
        except Exception as e:
            print(f"  ✗ Error al inicializar Gemini: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Error al inicializar Gemini. Verifica tu API key: {str(e)}'
            }), 500
        
        # Paso 1: Realizar scraping
        print("\n🔍 Iniciando scraping...")
        raw_products = scraper.search_products(product_name)
        
        if not raw_products:
            print("⚠ No se encontraron productos")
            return jsonify({
                'success': False,
                'error': 'No se encontraron productos. Verifica tu API key de scraping o intenta con otro término de búsqueda.'
            }), 404
        
        print(f"✓ Scraping completado: {len(raw_products)} productos encontrados")
        
        # Paso 2: Analizar con Gemini
        print("\n🤖 Iniciando análisis con Gemini...")
        analysis_result = analyzer.analyze_products(raw_products, product_name)
        
        if not analysis_result:
            print("✗ Error en el análisis de Gemini")
            return jsonify({
                'success': False,
                'error': 'Error al analizar los productos con Gemini. Verifica tu API key.'
            }), 500
        
        print("✓ Análisis completado exitosamente")
        
        # Paso 3: Devolver resultados
        print("\n📊 Preparando respuesta...")
        print("="*50)
        print("✅ Búsqueda completada exitosamente")
        print("="*50 + "\n")
        
        return jsonify({
            'success': True,
            'data': {
                'summary': analysis_result.get('summary', ''),
                'products': analysis_result.get('products', []),
                'statistics': analysis_result.get('statistics', {})
            }
        })
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {str(e)}")
        print(traceback.format_exc())
        print("="*50 + "\n")
        return jsonify({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }), 500

@main_bp.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint para verificar el estado del servidor"""
    return jsonify({
        'status': 'healthy',
        'message': 'PriceFinder IA está funcionando correctamente'
    })

@main_bp.route('/static/<path:filename>')
def serve_static(filename):
    """Servir archivos estáticos (fallback para Vercel)"""
    from flask import send_from_directory
    import os
    static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'static')
    return send_from_directory(static_folder, filename)