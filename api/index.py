import sys
from pathlib import Path

# Add project root to sys.path so web package is discoverable
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from web.server import app

# Vercel Serverless Function entry point
# Exposes the WSGI application as 'app'
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)

