"""
MediConnect HMS — Unified Root Launcher
Starts the FastAPI + Uvicorn backend and serves the frontend.
"""

import sys
import os
import webbrowser

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import uvicorn

def main():
    print("=" * 65)
    print("  MediConnect HMS - FastAPI & Uvicorn Application")
    print("=" * 65)
    print("  Web Application : http://localhost:8000")
    print("  API Swagger Docs: http://localhost:8000/docs")
    print("  Frontend Folder : mediconnect3/frontend/")
    print("  Backend Folder  : mediconnect3/backend/")
    print("=" * 65)

    try:
        webbrowser.open("http://localhost:8000")
    except Exception:
        pass

    os.chdir(backend_dir)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
