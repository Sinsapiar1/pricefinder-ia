#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión con Gemini
"""
import google.generativeai as genai
import sys

def test_gemini_connection(api_key):
    """Prueba la conexión con Gemini"""
    print("🧪 Probando conexión con Gemini...")
    print("-" * 50)
    
    try:
        # Configurar Gemini
        genai.configure(api_key=api_key)
        print("✓ API Key configurada")
        
        # Probar diferentes modelos
        models_to_test = [
            'gemini-1.5-flash-latest',
            'gemini-1.5-flash',
            'gemini-pro',
            'gemini-1.0-pro'
        ]
        
        successful_model = None
        
        for model_name in models_to_test:
            print(f"\n🔄 Probando modelo: {model_name}...")
            try:
                model = genai.GenerativeModel(model_name)
                
                # Hacer una prueba simple
                print("  📤 Enviando prompt de prueba...")
                response = model.generate_content("Responde solo con: OK")
                
                print(f"  📥 Respuesta: {response.text[:100]}")
                print(f"  ✅ ¡Modelo {model_name} funciona!")
                successful_model = model_name
                break
                
            except Exception as e:
                print(f"  ❌ Error con {model_name}: {str(e)}")
                continue
        
        if successful_model:
            print("\n" + "=" * 50)
            print(f"✅ ¡CONEXIÓN EXITOSA!")
            print(f"Modelo recomendado: {successful_model}")
            print("=" * 50)
            return True
        else:
            print("\n" + "=" * 50)
            print("❌ NINGÚN MODELO FUNCIONÓ")
            print("=" * 50)
            raise Exception("No se pudo conectar con ningún modelo de Gemini")
        
    except Exception as e:
        print(f"\n❌ Error general: {str(e)}")
        print("\n💡 Posibles causas:")
        print("  1. API key inválida o expirada")
        print("  2. Límite de solicitudes excedido (cuenta gratuita)")
        print("  3. API de Gemini no habilitada en tu cuenta")
        print("  4. Problemas de conexión a internet")
        print("\n🔧 Soluciones:")
        print("  1. Verifica tu API key en: https://ai.google.dev/")
        print("  2. Genera una nueva API key")
        print("  3. Espera unos minutos si excediste el límite")
        print("  4. Verifica que la API esté habilitada en tu proyecto")
        return False

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  TEST DE CONEXIÓN CON GOOGLE GEMINI")
    print("=" * 50 + "\n")
    
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = input("Ingresa tu Gemini API Key: ").strip()
    
    if not api_key:
        print("❌ No se proporcionó una API key")
        sys.exit(1)
    
    success = test_gemini_connection(api_key)
    sys.exit(0 if success else 1)