"""
MediConnect Backend Server Launcher (FastAPI + Uvicorn)
"""

import sys
import os

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import uvicorn

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    print("=" * 65)
    print("  MediConnect HMS - FastAPI + Uvicorn Backend Server")
    print("  Host: http://localhost:8000")
    print("  API Docs (Swagger): http://localhost:8000/docs")
    print("  Frontend UI: http://localhost:8000")
    print("=" * 65)

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
