"""
Vercel serverless function handler for Flask app
"""
import os
import sys

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from config import Config

# Create Flask app
app = create_app()

# Vercel handler
def handler(request):
    """Main handler for Vercel serverless functions"""
    return app(request.environ, lambda *args: None)

# For local development
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)