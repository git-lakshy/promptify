import sys
import os
from pathlib import Path

# Auto-detect backend directory and add it to sys.path
# This allows 'uvicorn main:app' to work from the project root
backend_root = Path(__file__).parent / "backend"
if backend_root.exists():
    sys.path.append(str(backend_root))

try:
    from app.main import app
except ImportError as e:
    print(f"Error: Could not import 'app.main'. Ensure you are running from the project root or backend folder.")
    print(f"Current Path: {os.getcwd()}")
    print(f"Python Path: {sys.path}")
    raise e

if __name__ == "__main__":
    import uvicorn
    # Use the application instance directly when run as a script
    uvicorn.run(app, host="0.0.0.0", port=8000)
