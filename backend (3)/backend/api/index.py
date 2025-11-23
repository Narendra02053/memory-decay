# Vercel serverless function entry point for FastAPI
import sys
from pathlib import Path

# Add parent directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Import the FastAPI app
from app import app

# Export for Vercel
handler = app
