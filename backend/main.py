import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routers import (
    auth,
    departments,
    doctors,
    patients,
    appointments,
    prescriptions,
    lab,
    admin,
    share_links,
    chat
)

from db import init_db
from config import FRONTEND_DIR

# Initialize database schema and seeds
init_db()

app = FastAPI(
    title="MediConnect HMS API",
    description="FastAPI + Uvicorn backend for MediConnect Hospital Management System",
    version="2.5.0"
)

# ── CORS Middleware ───────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Health Check ──────────────────────────────────────────────────────────────
@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "database": "mediconnect.db",
        "type": "sqlite3",
        "framework": "FastAPI",
        "server": "Uvicorn"
    }

# ── API Routers ───────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(departments.router)
app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(prescriptions.router)
app.include_router(lab.router)
app.include_router(admin.router)
app.include_router(share_links.router)
app.include_router(chat.router)

# ── Static Frontend Serving ───────────────────────────────────────────────────
if os.path.exists(FRONTEND_DIR):
    vendor_dir = os.path.join(FRONTEND_DIR, "vendor")
    
    if os.path.exists(vendor_dir):
        app.mount("/vendor", StaticFiles(directory=vendor_dir), name="vendor")

    @app.get("/", tags=["Frontend"])
    def serve_frontend_root():
        index_file = os.path.join(FRONTEND_DIR, "index.html")
        return FileResponse(index_file)

    @app.get("/{catchall:path}", tags=["Frontend"])
    def serve_frontend_catchall(catchall: str):
        # If it's an API route that 404'd, don't return HTML
        if catchall.startswith("api/"):
            return {"error": f"API route not found: /{catchall}"}
        
        # Check if requested file exists in frontend
        requested_file = os.path.join(FRONTEND_DIR, catchall)
        if os.path.isfile(requested_file):
            return FileResponse(requested_file)
        
        # Fallback to SPA index.html
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
