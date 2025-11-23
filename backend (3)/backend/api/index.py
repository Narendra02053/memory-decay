# Vercel serverless function for FastAPI
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app

# Vercel Python runtime automatically detects FastAPI app
# Just import and expose it
