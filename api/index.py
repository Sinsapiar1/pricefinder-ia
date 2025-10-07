"""
Vercel Serverless Function Handler for Flask App
"""
import sys
import os

# Agregar el directorio raíz al path de Python
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Importar y crear la aplicación Flask
from app import create_app

# Crear la aplicación
app = create_app()

# Handler para Vercel (WSGI)
# Vercel detectará automáticamente 'app' como WSGI application
