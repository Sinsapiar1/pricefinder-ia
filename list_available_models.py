#!/usr/bin/env python3
"""
Script para listar TODOS los modelos disponibles en tu cuenta de Gemini
"""
import google.generativeai as genai
import sys

def list_available_models(api_key):
    """Lista todos los modelos disponibles"""
    print("\n" + "=" * 70)
    print("  LISTANDO MODELOS DISPONIBLES EN TU CUENTA GEMINI")
    print("=" * 70 + "\n")
    
    try:
        # Configurar Gemini
        genai.configure(api_key=api_key)
        print("✓ API Key configurada\n")
        
        # Listar todos los modelos
        print("🔍 Buscando modelos disponibles...")
        print("-" * 70)
        
        models = genai.list_models()
        
        available_models = []
        generate_content_models = []
        
        for model in models:
            available_models.append(model.name)
            
            # Verificar si soporta generateContent
            if 'generateContent' in model.supported_generation_methods:
                generate_content_models.append(model.name)
                print(f"\n✅ {model.name}")
                print(f"   📝 Nombre para código: {model.name.replace('models/', '')}")
                print(f"   📋 Descripción: {getattr(model, 'description', 'N/A')[:100]}")
                print(f"   🎯 Métodos: {', '.join(model.supported_generation_methods)}")
                
                # Límites
                if hasattr(model, 'input_token_limit'):
                    print(f"   📊 Tokens entrada: {model.input_token_limit}")
                if hasattr(model, 'output_token_limit'):
                    print(f"   📊 Tokens salida: {model.output_token_limit}")
        
        print("\n" + "=" * 70)
        
        if generate_content_models:
            print(f"\n✅ MODELOS DISPONIBLES PARA generateContent: {len(generate_content_models)}")
            print("\n📋 Lista de modelos que puedes usar:")
            for model in generate_content_models:
                model_name = model.replace('models/', '')
                print(f"   • {model_name}")
            
            # Recomendar el mejor
            recommended = generate_content_models[0].replace('models/', '')
            print(f"\n🎯 MODELO RECOMENDADO: {recommended}")
            
            print("\n📝 USO EN TU CÓDIGO:")
            print(f"   En gemini_analyzer.py, usa:")
            print(f"   self.model = genai.GenerativeModel('{recommended}')")
            
            print("\n✅ PRUEBA RÁPIDA:")
            print(f"   Probando modelo recomendado: {recommended}...")
            
            try:
                test_model = genai.GenerativeModel(recommended)
                response = test_model.generate_content("Di 'OK'")
                print(f"   ✅ ¡Funciona! Respuesta: {response.text[:50]}")
            except Exception as e:
                print(f"   ⚠️  Error al probar: {str(e)}")
            
        else:
            print("\n❌ NO HAY MODELOS DISPONIBLES PARA generateContent")
            
            if available_models:
                print(f"\n⚠️  Se encontraron {len(available_models)} modelos, pero ninguno soporta generateContent:")
                for model in available_models[:5]:
                    print(f"   • {model}")
            else:
                print("\n❌ NO SE ENCONTRÓ NINGÚN MODELO EN TU CUENTA")
                print("\n🔧 ACCIÓN REQUERIDA:")
                print("   1. Ve a https://console.cloud.google.com/")
                print("   2. Selecciona tu proyecto")
                print("   3. Busca 'Generative Language API'")
                print("   4. Haz clic en 'ENABLE' (Habilitar)")
                print("   5. Espera 2-3 minutos")
                print("   6. Vuelve a ejecutar este script")
        
        print("\n" + "=" * 70 + "\n")
        return len(generate_content_models) > 0
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\n🔧 Posibles causas:")
        print("   1. API key inválida")
        print("   2. Generative Language API no habilitada")
        print("   3. Proyecto de Google Cloud mal configurado")
        print("   4. Problemas de red")
        
        print("\n📚 Recursos:")
        print("   • Consola: https://console.cloud.google.com/")
        print("   • API Studio: https://ai.google.dev/")
        print("   • Documentación: https://ai.google.dev/docs")
        
        return False

if __name__ == "__main__":
    print("\n🔑 Necesitarás tu API key de Gemini")
    
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = input("\nIngresa tu Gemini API Key: ").strip()
    
    if not api_key:
        print("❌ No se proporcionó una API key")
        sys.exit(1)
    
    success = list_available_models(api_key)
    
    if success:
        print("✅ ¡Listo! Copia el modelo recomendado y úsalo en tu código.")
    else:
        print("⚠️  Sigue las instrucciones anteriores para habilitar la API.")
    
    sys.exit(0 if success else 1)