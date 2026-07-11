import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent

from app import database
from app.routers import auth, comparison, documentation, metrics, model_api, users, assessments

# Define the app
app = FastAPI()

frontend_origins = [
    origin.strip()
    for origin in os.getenv("FRONTEND_ORIGINS", "").split(",")
    if origin.strip()
]
if frontend_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=frontend_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/health/db")
async def database_health_check():
    url = database.DATABASE_URL
    backend = "sqlite" if url.startswith("sqlite") else "postgres"
    return {
        "status": "ok",
        "backend": backend,
        "using_local_fallback": backend == "sqlite",
    }

# Include the database-backed routers you already started.
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(documentation.router)
app.include_router(comparison.router)
app.include_router(metrics.router)
app.include_router(model_api.router)
app.include_router(assessments.router)

# Include server.py-compatible /api/... routes used by the current frontend.
app.include_router(documentation.api_router)
app.include_router(metrics.api_router)
app.include_router(model_api.api_router)



# Serve index.html, app.js, styles.css, assets/, examples/, etc. from the same
# project root that server.py used to host through SimpleHTTPRequestHandler.
app.mount("/", StaticFiles(directory=PROJECT_ROOT, html=True), name="static")
