import sys
import os

# Append the absolute path of the backend directory to sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
sys.path.insert(0, backend_dir)

# Import the Flask application instance
from app import app
