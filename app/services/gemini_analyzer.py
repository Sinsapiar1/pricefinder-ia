import google.generativeai as genai
import json
import re

class GeminiAnalyzer:
    """Servicio para analizar productos usando Google Gemini"""
    
    def __init__(self, api_key):
        try:
            genai.configure(api_key=api_key)
            
            # Usar el modelo más simple y compatible - SIN prefijos
            # Este modelo funciona en TODAS las versiones de la API
            model_name = 'gemini-1.5-flash'
            
            try:
                self.model = genai.GenerativeModel(model_name)
                print(f"✓ Gemini configurado exitosamente con: {model_name}")
            except Exception as e:
                # Fallback al modelo clásico si falla
                print(f"⚠ {model_name} no disponible, intentando gemini-pro...")
                model_name = 'gemini-pro'
                self.model = genai.GenerativeModel(model_name)
                print(f"✓ Gemini configurado con fallback: {model_name}")
                    
        except Exception as e:
            error_msg = str(e)
            print(f"✗ Error al configurar Gemini: {error_msg}")
            
            # Mensaje de ayuda específico
            if 'API key' in error_msg or 'invalid' in error_msg.lower():
                raise Exception("API key de Gemini inválida. Genera una nueva en https://aistudio.google.com/app/apikey")
            elif 'not found' in error_msg.lower():
                raise Exception("Modelo no disponible. Tu API key de Gemini puede no tener acceso. Intenta generar una nueva key.")
            else:
                raise Exception(f"Error al inicializar Gemini: {error_msg}")
    
    def analyze_products(self, raw_products, product_name):
        """
        Analiza productos crudos y genera recomendaciones
        
        Args:
            raw_products (list): Lista de productos sin procesar
            product_name (str): Nombre del producto buscado
            
        Returns:
            dict: Análisis completo con productos normalizados y resumen
        """
        if not raw_products:
            return None
        
        # Construir el prompt para Gemini
        prompt = self._build_analysis_prompt(raw_products, product_name)
        
        try:
            # Llamar a Gemini
            print("🤖 Enviando prompt a Gemini...")
            print(f"   Productos a analizar: {len(raw_products)}")
            
            # Configuración para mejor compatibilidad
            generation_config = {
                'temperature': 0.7,
                'top_p': 0.8,
                'top_k': 40,
                'max_output_tokens': 2048,
            }
            
            print("   Generando contenido...")
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            print(f"✓ Respuesta recibida de Gemini")
            
            # Verificar si hay respuesta
            if not response or not hasattr(response, 'text'):
                print("✗ Gemini no devolvió respuesta válida")
                raise Exception("Gemini no devolvió respuesta válida. Verifica tu API key.")
            
            # Extraer el JSON de la respuesta
            print("   Parseando respuesta JSON...")
            analysis = self._parse_gemini_response(response.text)
            
            if not analysis:
                print("✗ No se pudo parsear la respuesta de Gemini")
                raise Exception("No se pudo parsear la respuesta de Gemini")
            
            if not analysis.get('products'):
                print("✗ La respuesta de Gemini no contiene productos")
                raise Exception("La respuesta de Gemini no contiene productos")
            
            # Calcular estadísticas
            print("   Calculando estadísticas...")
            statistics = self._calculate_statistics(analysis.get('products', []))
            analysis['statistics'] = statistics
            
            print(f"✓ Análisis completado: {len(analysis.get('products', []))} productos procesados")
            return analysis
            
        except Exception as e:
            print(f"✗ Error al analizar con Gemini: {str(e)}")
            import traceback
            print(traceback.format_exc())
            raise  # Re-raise para que el caller maneje el error
    
    def _build_analysis_prompt(self, products, product_name):
        """Construye un prompt SIMPLE y EFECTIVO para Gemini"""
        
        # Prompt más corto y directo para mejor rendimiento
        prompt = f"""Analiza estos productos y devuelve SOLO JSON válido (sin texto extra):

PRODUCTO BUSCADO: {product_name}

PRODUCTOS:
{json.dumps(products, indent=2, ensure_ascii=False)}

DEVUELVE JSON con esta estructura exacta:
{{
  "summary": "Resumen con recomendación principal y % de ahorro",
  "insights": [
    "Observación 1 sobre precios",
    "Observación 2 sobre valor",
    "Observación 3 sobre recomendación"
  ],
  "products": [
    {{
      "tienda": "tienda_original",
      "nombre_normalizado": "Nombre normalizado",
      "nombre_crudo": "nombre_original",
      "precio": precio_numero,
      "url": "url_original",
      "reviews": reviews_numero,
      "categoria": "Idéntico",
      "condicion": "Nuevo",
      "especificaciones_detectadas": ["spec1"],
      "recomendacion": "🏆 Mejor Opción",
      "razon": "Razón breve",
      "valor_score": 85,
      "precio_vs_promedio": "-15%"
    }}
  ]
}}

REGLAS:
- "🏆 Mejor Opción" = precio más bajo
- "✅ Buena Alternativa" = precio razonable  
- "⚠️ Considerar" = precio alto
- "❌ No Recomendado" = precio excesivo
- Calcula precio_vs_promedio para cada producto
- Genera 3 insights útiles"""
        
        return prompt
    
    def _parse_gemini_response(self, response_text):
        """Extrae y parsea el JSON de la respuesta de Gemini"""
        try:
            print(f"📄 Respuesta de Gemini (primeros 200 chars): {response_text[:200]}")
            
            # Limpiar la respuesta
            cleaned_text = response_text.strip()
            
            # Remover markdown code blocks si existen
            if cleaned_text.startswith('```'):
                # Extraer contenido entre ```json y ```
                lines = cleaned_text.split('\n')
                cleaned_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else cleaned_text
                cleaned_text = cleaned_text.replace('```json', '').replace('```', '').strip()
            
            # Intentar encontrar el JSON en la respuesta
            # Buscar contenido entre llaves
            start_idx = cleaned_text.find('{')
            end_idx = cleaned_text.rfind('}')
            
            if start_idx != -1 and end_idx != -1:
                json_str = cleaned_text[start_idx:end_idx+1]
                analysis = json.loads(json_str)
                print(f"✓ JSON parseado exitosamente")
                return analysis
            else:
                # Si no se encuentra JSON, intentar parsear directamente
                print("⚠ Intentando parsear respuesta completa como JSON...")
                return json.loads(cleaned_text)
                
        except json.JSONDecodeError as e:
            print(f"✗ Error al parsear JSON de Gemini: {str(e)}")
            print(f"📄 Respuesta completa recibida:")
            print(response_text)
            print("-" * 50)
            
            # Fallback: devolver estructura básica con los productos originales
            print("⚠ Usando fallback: estructura básica")
            return {
                'summary': 'No se pudo generar un resumen automático. Revisa los resultados manualmente.',
                'products': []
            }
        except Exception as e:
            print(f"✗ Error inesperado al parsear respuesta: {str(e)}")
            return {
                'summary': 'Error al procesar la respuesta de Gemini.',
                'products': []
            }
    
    def _calculate_statistics(self, products):
        """Calcula estadísticas sobre los productos analizados"""
        if not products:
            return {}
        
        prices = [p['precio'] for p in products if p.get('precio')]
        
        if not prices:
            return {}
        
        avg_price = sum(prices) / len(prices)
        min_price = min(prices)
        max_price = max(prices)
        
        # Contar recomendaciones
        best_price_count = sum(1 for p in products if p.get('recomendacion') == 'Mejor Precio')
        alternative_count = sum(1 for p in products if p.get('recomendacion') == 'Alternativa')
        not_recommended_count = sum(1 for p in products if p.get('recomendacion') == 'No Recomendado')
        
        return {
            'precio_promedio': round(avg_price, 2),
            'precio_minimo': round(min_price, 2),
            'precio_maximo': round(max_price, 2),
            'rango_precio': round(max_price - min_price, 2),
            'total_productos': len(products),
            'mejores_precios': best_price_count,
            'alternativas': alternative_count,
            'no_recomendados': not_recommended_count
        }