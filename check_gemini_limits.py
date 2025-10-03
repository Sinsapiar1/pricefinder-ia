#!/usr/bin/env python3
"""
Script para verificar límites y cuota de Google Gemini (cuenta gratuita)
"""
import google.generativeai as genai
import sys
import time

def check_gemini_limits(api_key):
    """Verifica los límites de la cuenta de Gemini"""
    print("\n" + "=" * 60)
    print("  VERIFICACIÓN DE CUENTA GOOGLE GEMINI")
    print("=" * 60 + "\n")
    
    try:
        # Configurar Gemini
        genai.configure(api_key=api_key)
        print("✓ API Key configurada\n")
        
        # Información de cuenta gratuita
        print("📊 LÍMITES DE CUENTA GRATUITA:")
        print("-" * 60)
        print("• Solicitudes por minuto (RPM): 15")
        print("• Solicitudes por día (RPD): 1,500")
        print("• Tokens por minuto (TPM): 1,000,000")
        print("• Tokens de entrada por solicitud: 32,760")
        print("• Tokens de salida por solicitud: 8,192")
        print("-" * 60 + "\n")
        
        # Probar modelos disponibles
        print("🔍 PROBANDO MODELOS DISPONIBLES:")
        print("-" * 60)
        
        models_to_test = [
            ('gemini-1.5-flash-latest', 'Recomendado para cuenta gratuita'),
            ('gemini-1.5-flash', 'Flash standard'),
            ('gemini-pro', 'Pro legacy'),
            ('gemini-1.0-pro', 'Versión 1.0')
        ]
        
        working_models = []
        
        for model_name, description in models_to_test:
            print(f"\n🧪 Probando: {model_name}")
            print(f"   Descripción: {description}")
            
            try:
                model = genai.GenerativeModel(model_name)
                
                # Test simple
                start_time = time.time()
                response = model.generate_content(
                    "Responde con OK",
                    generation_config={'max_output_tokens': 10}
                )
                elapsed_time = time.time() - start_time
                
                print(f"   ✅ FUNCIONA")
                print(f"   ⏱️  Tiempo de respuesta: {elapsed_time:.2f}s")
                print(f"   📝 Respuesta: {response.text[:50]}")
                working_models.append(model_name)
                
                # Esperar un poco para no exceder rate limit
                time.sleep(1)
                
            except Exception as e:
                error_msg = str(e)
                print(f"   ❌ ERROR: {error_msg}")
                
                # Detectar tipo de error
                if "quota" in error_msg.lower() or "limit" in error_msg.lower():
                    print("   ⚠️  Has excedido el límite de la cuenta gratuita")
                    print("   💡 Espera unos minutos e intenta nuevamente")
                elif "not found" in error_msg.lower() or "invalid" in error_msg.lower():
                    print("   ⚠️  Modelo no disponible con tu cuenta")
                
        print("\n" + "=" * 60)
        
        if working_models:
            print("\n✅ MODELOS DISPONIBLES EN TU CUENTA:")
            for model in working_models:
                print(f"   • {model}")
            print(f"\n🎯 RECOMENDACIÓN: Usa '{working_models[0]}' en la aplicación")
            
            print("\n📋 SIGUIENTE PASO:")
            print(f"   En app/services/gemini_analyzer.py, usa:")
            print(f"   self.model = genai.GenerativeModel('{working_models[0]}')")
        else:
            print("\n❌ NO HAY MODELOS DISPONIBLES")
            print("\n🔧 POSIBLES SOLUCIONES:")
            print("   1. Genera una nueva API Key en https://ai.google.dev/")
            print("   2. Verifica que la API esté habilitada")
            print("   3. Espera unos minutos si excediste el límite")
            print("   4. Revisa que tu cuenta esté activa")
        
        print("\n" + "=" * 60)
        print("✅ Verificación completada")
        print("=" * 60 + "\n")
        
        return len(working_models) > 0
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {str(e)}")
        print("\n🔗 Recursos útiles:")
        print("   • Obtener API Key: https://ai.google.dev/")
        print("   • Documentación: https://ai.google.dev/docs")
        print("   • Límites de cuota: https://ai.google.dev/pricing")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = input("🔑 Ingresa tu Gemini API Key: ").strip()
    
    if not api_key:
        print("❌ No se proporcionó una API key")
        sys.exit(1)
    
    success = check_gemini_limits(api_key)
    sys.exit(0 if success else 1)