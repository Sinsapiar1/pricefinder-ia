from flask import Blueprint, render_template, request, jsonify
from app.services.scraper import ProductScraper
from app.services.gemini_analyzer import GeminiAnalyzer
from config import Config
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
        
        # Inicializar servicios con mejor manejo de errores
        print("\n📡 Inicializando servicios...")
        
        # Importar y validar módulos
        try:
            print("  → Importando módulos...")
            scraper = ProductScraper(scraper_key)
            print("  ✓ Scraper inicializado")
        except ImportError as e:
            print(f"  ✗ Error de importación: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Error al cargar módulos necesarios: {str(e)}'
            }), 500
        except Exception as e:
            print(f"  ✗ Error al inicializar scraper: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return jsonify({
                'success': False,
                'error': f'Error al inicializar el servicio de scraping: {str(e)}'
            }), 500
        
        try:
            print("  → Inicializando Gemini...")
            analyzer = GeminiAnalyzer(gemini_key)
            print("  ✓ Gemini inicializado")
        except ImportError as e:
            print(f"  ✗ Error de importación Gemini: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Error al cargar Google Generative AI. Módulo no disponible: {str(e)}'
            }), 500
        except Exception as e:
            print(f"  ✗ Error al inicializar Gemini: {str(e)}")
            import traceback
            print(traceback.format_exc())
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
        'message': 'PriceFinder IA está funcionando correctamente',
        'version': '1.0',
        'environment': 'production'
    })

@main_bp.route('/api/test', methods=['POST'])
def test_apis():
    """Endpoint para probar las API keys sin hacer scraping completo"""
    try:
        data = request.get_json()
        gemini_key = data.get('gemini_api_key', '').strip()
        scraper_key = data.get('scraper_api_key', '').strip()
        
        results = {
            'gemini': 'not_tested',
            'scraper': 'not_tested'
        }
        
        # Probar Gemini
        if gemini_key:
            try:
                from app.services.gemini_analyzer import GeminiAnalyzer
                analyzer = GeminiAnalyzer(gemini_key)
                results['gemini'] = 'valid'
            except Exception as e:
                results['gemini'] = f'error: {str(e)}'
        
        # Probar Scraper (sin hacer request real)
        if scraper_key:
            results['scraper'] = 'provided' if len(scraper_key) > 10 else 'invalid_length'
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main_bp.route('/static/<path:filename>')
def serve_static(filename):
    """Servir archivos estáticos (fallback para Vercel)"""
    from flask import send_from_directory
    import os
    static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'static')
    return send_from_directory(static_folder, filename)

@main_bp.route('/api/debug', methods=['GET'])
def debug_info():
    """Endpoint de debug para verificar la configuración"""
    import sys
    import os
    
    try:
        import google.generativeai as genai
        gemini_available = True
        gemini_version = getattr(genai, '__version__', 'unknown')
    except:
        gemini_available = False
        gemini_version = 'not installed'
    
    try:
        import requests
        requests_available = True
    except:
        requests_available = False
    
    try:
        import bs4
        bs4_available = True
    except:
        bs4_available = False
    
    return jsonify({
        'status': 'debug',
        'python_version': sys.version,
        'cwd': os.getcwd(),
        'modules': {
            'google-generativeai': {
                'available': gemini_available,
                'version': gemini_version
            },
            'requests': {'available': requests_available},
            'beautifulsoup4': {'available': bs4_available}
        },
        'config': {
            'target_sites': Config.TARGET_SITES,
            'max_results': Config.MAX_RESULTS_PER_SITE,
            'timeout': Config.REQUEST_TIMEOUT
        }
    })