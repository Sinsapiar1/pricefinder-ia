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

app = create_app()

# Este es el punto de entrada para Vercel
# Vercel automáticamente manejará las requests usando esta variable 'app'
