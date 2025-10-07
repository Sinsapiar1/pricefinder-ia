"""
Punto de entrada para Vercel Serverless Functions
"""
import sys
import os

# Añadir el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

# Crear la aplicación Flask
app = create_app()

# Esta es la función que Vercel llamará
def handler(request, context):
    return app(request, context)

# Para compatibilidad con WSGI
application = app
