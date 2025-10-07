"""
Vercel serverless function handler for Flask app
"""
import os
import sys

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

# Create Flask app
app = create_app()

# Vercel handler - debe ser 'app' directamente
# Vercel automáticamente detecta la variable 'app'
