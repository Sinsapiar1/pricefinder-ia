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

@main_bp.route('/test')
def test_page():
    """Página de testing para verificar scraping por tienda"""
    return render_template('test.html')

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
        try:
            raw_products = scraper.search_products(product_name)
            print(f"✓ Scraping completado: {len(raw_products)} productos encontrados")
        except Exception as scraper_error:
            print(f"✗ Error en scraping: {str(scraper_error)}")
            return jsonify({
                'success': False,
                'error': f'Error al hacer scraping: {str(scraper_error)}. Verifica tu Scraper API key.'
            }), 500
        
        if not raw_products:
            print("⚠ No se encontraron productos")
            return jsonify({
                'success': False,
                'error': 'No se encontraron productos. Posibles causas: API key de ScraperAPI incorrecta, límite de requests alcanzado, o el producto no existe en las tiendas.'
            }), 404
        
        # Paso 2: Analizar con Gemini
        print("\n🤖 Iniciando análisis con Gemini...")
        try:
            analysis_result = analyzer.analyze_products(raw_products, product_name)
            print("✓ Análisis completado exitosamente")
        except Exception as gemini_error:
            print(f"✗ Error en Gemini: {str(gemini_error)}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'success': False,
                'error': f'Error al analizar con Gemini: {str(gemini_error)}. Verifica tu Gemini API key en https://aistudio.google.com/'
            }), 500
        
        if not analysis_result:
            print("✗ Gemini devolvió resultado vacío")
            return jsonify({
                'success': False,
                'error': 'Gemini no pudo analizar los productos. Intenta nuevamente.'
            }), 500
        
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
    """Endpoint para probar scraping de cada tienda individualmente"""
    try:
        data = request.get_json()
        scraper_key = data.get('scraper_api_key', '').strip()
        product_name = data.get('product_name', 'iPhone 15').strip()
        
        if not scraper_key:
            return jsonify({
                'success': False,
                'error': 'Se requiere Scraper API Key'
            }), 400
        
        from app.services.scraper import ProductScraper
        scraper = ProductScraper(scraper_key)
        
        # Probar cada tienda individualmente
        results = {}
        for site in ['amazon.com', 'ebay.com', 'walmart.com', 'bestbuy.com']:
            print(f"\n🧪 TESTING {site}...")
            try:
                products = scraper._search_site(site, product_name)
                results[site] = {
                    'status': 'success',
                    'products_found': len(products),
                    'products': products[:2] if products else []  # Solo primeros 2 para preview
                }
                print(f"✓ {site}: {len(products)} productos")
            except Exception as e:
                results[site] = {
                    'status': 'error',
                    'error': str(e)[:200],
                    'products_found': 0
                }
                print(f"✗ {site}: {str(e)[:100]}")
        
        return jsonify({
            'success': True,
            'test_results': results,
            'summary': {
                'amazon': results.get('amazon.com', {}).get('products_found', 0),
                'ebay': results.get('ebay.com', {}).get('products_found', 0),
                'walmart': results.get('walmart.com', {}).get('products_found', 0),
                'bestbuy': results.get('bestbuy.com', {}).get('products_found', 0)
            }
        })
        
    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@main_bp.route('/static/<path:filename>')
def serve_static(filename):
    """Servir archivos estáticos (fallback para Vercel)"""
    from flask import send_from_directory, current_app
    import os
    
    try:
        # Usar la configuración de static_folder de Flask
        static_folder = current_app.static_folder
        print(f"[STATIC] Sirviendo: {filename} desde {static_folder}")
        
        # Verificar que el archivo existe
        file_path = os.path.join(static_folder, filename)
        if not os.path.exists(file_path):
            print(f"[STATIC] ERROR: Archivo no encontrado: {file_path}")
            return jsonify({'error': 'Archivo no encontrado'}), 404
        
        return send_from_directory(static_folder, filename)
    except Exception as e:
        print(f"[STATIC] ERROR: {str(e)}")
        return jsonify({'error': str(e)}), 500

@main_bp.route('/api/debug', methods=['GET'])
def debug_info():
    """Endpoint de debug para verificar la configuración"""
    from flask import current_app
    import sys
    import os
    
    try:
        import google.generativeai as genai
        gemini_available = True
        gemini_version = getattr(genai, '__version__', 'unknown')
    except Exception as e:
        gemini_available = False
        gemini_version = f'error: {str(e)}'
    
    try:
        import requests
        requests_available = True
        requests_version = requests.__version__
    except Exception as e:
        requests_available = False
        requests_version = f'error: {str(e)}'
    
    try:
        import bs4
        bs4_available = True
        bs4_version = bs4.__version__
    except Exception as e:
        bs4_available = False
        bs4_version = f'error: {str(e)}'
    
    # Información de paths
    app_dir = os.path.dirname(os.path.abspath(__file__))
    static_folder = current_app.static_folder
    template_folder = current_app.template_folder
    
    # Verificar existencia de archivos críticos
    static_files = {}
    if os.path.exists(static_folder):
        for root, dirs, files in os.walk(static_folder):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), static_folder)
                static_files[rel_path] = True
    
    return jsonify({
        'status': 'healthy',
        'environment': 'vercel' if 'VERCEL' in os.environ else 'local',
        'python_version': sys.version.split()[0],
        'cwd': os.getcwd(),
        'paths': {
            'app_dir': app_dir,
            'static_folder': static_folder,
            'template_folder': template_folder,
            'static_exists': os.path.exists(static_folder),
            'templates_exists': os.path.exists(template_folder)
        },
        'static_files': static_files,
        'modules': {
            'google-generativeai': {
                'available': gemini_available,
                'version': gemini_version
            },
            'requests': {
                'available': requests_available,
                'version': requests_version
            },
            'beautifulsoup4': {
                'available': bs4_available,
                'version': bs4_version
            }
        },
        'config': {
            'target_sites': Config.TARGET_SITES,
            'max_results': Config.MAX_RESULTS_PER_SITE,
            'timeout': Config.REQUEST_TIMEOUT
        },
        'routes': [str(rule) for rule in current_app.url_map.iter_rules()]
    })