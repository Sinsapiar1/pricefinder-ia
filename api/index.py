import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from app import create_app
    app = create_app()
    print("✓ Flask app created successfully")
except Exception as e:
    print(f"✗ Error creating Flask app: {e}")
    import traceback
    traceback.print_exc()
    raise
