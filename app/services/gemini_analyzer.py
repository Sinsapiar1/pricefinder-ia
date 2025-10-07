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
        """Construye el prompt MEJORADO para análisis inteligente con Gemini"""
        
        prompt = f"""Eres un experto analista de productos y precios. Analiza estos productos con INTELIGENCIA PROFUNDA.

🎯 PRODUCTO BUSCADO: {product_name}

📦 PRODUCTOS ENCONTRADOS:
{json.dumps(products, indent=2, ensure_ascii=False)}

🧠 ANÁLISIS REQUERIDO:
1. Identifica productos IDÉNTICOS (mismo modelo/versión)
2. Detecta productos SIMILARES (alternativas válidas)
3. Identifica especificaciones clave en los nombres
4. Detecta condición: nuevo, reacondicionado, usado
5. Calcula valor real (precio/características)
6. Identifica ofertas excepcionales o precios sospechosos

📊 DEVOLVER JSON (sin texto adicional):
{{
  "summary": "Análisis inteligente: [insight principal]. Encontrados [N] productos idénticos y [M] alternativas. [Recomendación específica con % de ahorro]",
  "insights": [
    "Insight 1: [Observación inteligente]",
    "Insight 2: [Comparación de valor]",
    "Insight 3: [Advertencia o recomendación]"
  ],
  "products": [
    {{
      "tienda": "nombre_tienda",
      "nombre_normalizado": "Nombre estandarizado del producto",
      "nombre_crudo": "nombre original",
      "precio": 0.00,
      "url": "url",
      "reviews": 0.0,
      "categoria": "Idéntico|Similar|Alternativa|Diferente",
      "condicion": "Nuevo|Reacondicionado|Usado|Desconocido",
      "especificaciones_detectadas": ["spec1", "spec2"],
      "recomendacion": "🏆 Mejor Opción|✅ Buena Alternativa|⚠️ Considerar|❌ No Recomendado",
      "razon": "Razón detallada con % de ahorro/sobrecosto",
      "valor_score": 0-100,
      "precio_vs_promedio": "+X%|-X%"
    }}
  ]
}}

🎯 CRITERIOS INTELIGENTES:
- 🏆 "Mejor Opción": Precio más bajo para producto idéntico O mejor valor precio/calidad
- ✅ "Buena Alternativa": Precio competitivo, buen valor
- ⚠️ "Considerar": Precio alto pero puede tener ventajas (garantía, vendedor oficial)
- ❌ "No Recomendado": Precio excesivo sin justificación o producto claramente inferior

💡 INSIGHTS: Genera 3 observaciones inteligentes sobre:
- Diferencias de precio entre tiendas para producto idéntico
- Alternativas que ofrecen mejor valor
- Advertencias sobre precios anormales o productos engañosos"""
        
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