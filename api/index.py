import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from mangum import Adapter

# Create a handler for Vercel using Mangum
handler = Adapter(app) 