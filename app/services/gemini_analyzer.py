import google.generativeai as genai
import json
import re

class GeminiAnalyzer:
    """Servicio para analizar productos usando Google Gemini"""
    
    def __init__(self, api_key):
        try:
            genai.configure(api_key=api_key)
            
            # Usar modelos con mejor cuota gratuita
            models_to_try = [
                'gemini-flash-latest',      # Mejor opción
                'gemini-2.5-flash',         # Alternativa
                'gemini-2.0-flash',         # Fallback
            ]
            
            for model_name in models_to_try:
                try:
                    self.model = genai.GenerativeModel(model_name)
                    print(f"✓ Gemini configurado: {model_name}")
                    break
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            raise
    
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
            
            # Configuración para mejor compatibilidad con cuenta gratuita
            generation_config = {
                'temperature': 0.7,
                'top_p': 0.8,
                'top_k': 40,
                'max_output_tokens': 2048,  # Limitar tokens para cuenta gratuita
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            print(f"✓ Respuesta recibida de Gemini")
            
            # Extraer el JSON de la respuesta
            analysis = self._parse_gemini_response(response.text)
            
            if not analysis or not analysis.get('products'):
                print("⚠ No se pudieron parsear productos de la respuesta")
                return None
            
            # Calcular estadísticas
            statistics = self._calculate_statistics(analysis.get('products', []))
            analysis['statistics'] = statistics
            
            print(f"✓ Análisis completado: {len(analysis.get('products', []))} productos procesados")
            return analysis
            
        except Exception as e:
            print(f"✗ Error al analizar con Gemini: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return None
    
    def _build_analysis_prompt(self, products, product_name):
        """Construye el prompt para enviar a Gemini"""
        
        # Prompt simplificado para mejor compatibilidad con cuenta gratuita
        prompt = f"""Analiza estos productos y devuelve SOLO JSON válido (sin texto adicional):

PRODUCTO BUSCADO: {product_name}

PRODUCTOS:
{json.dumps(products, indent=2, ensure_ascii=False)}

DEVOLVER JSON con esta estructura:
{{
  "summary": "El mejor precio para [producto] es $[precio] en [tienda], ahorrando X% vs promedio",
  "products": [
    {{
      "tienda": "...",
      "nombre_normalizado": "...",
      "nombre_crudo": "...",
      "precio": 0.00,
      "url": "...",
      "reviews": 0.0,
      "recomendacion": "Mejor Precio|Alternativa|No Recomendado",
      "razon": "..."
    }}
  ]
}}

REGLAS:
- Normaliza nombres de productos similares
- "Mejor Precio" = precio más bajo
- "Alternativa" = precio razonable
- "No Recomendado" = precio alto o producto usado sin ventaja
- Calcula % de ahorro vs precio promedio"""
        
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